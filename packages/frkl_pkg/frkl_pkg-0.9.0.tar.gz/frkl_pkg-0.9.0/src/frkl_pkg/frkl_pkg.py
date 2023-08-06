# -*- coding: utf-8 -*-

"""Main module."""
import copy
import logging
import os
import shutil
import subprocess
import sys
from distutils.spawn import find_executable

from plumbum import local
from six import string_types

from .defaults import DEFAULT_CONDA_INSTALL_PATH, LOOKUP_PATHS
from .utils.virtualenv_helpers import create_virtualenv
from frutils.tasks.tasks import DummyTaskDetail
from .utils.conda_helpers import install_miniconda

log = logging.getLogger("frkl-pkg")


class FrklPkg(object):
    def __init__(self, extra_lookup_paths=None):

        if isinstance(extra_lookup_paths, string_types):
            extra_lookup_paths = [extra_lookup_paths]

        if extra_lookup_paths:
            self._lookup_paths = extra_lookup_paths + LOOKUP_PATHS
        else:
            self._lookup_paths = copy.copy(LOOKUP_PATHS)

        if hasattr(sys, "frozen"):
            self.frozen = True
            self.anaconda = False
            self.virtualenv = False
            self.conda = False
            self.python_version = None
            self._lookup_path_frozen = [sys._MEIPASS]
            # self._lookup_paths.append(sys._MEIPASS)

        else:
            self.frozen = False
            self._lookup_path_frozen = []

            current_python = local["python"]

            rc, stdout, stderr = current_python.run("--version")
            if stdout:
                current_python_version = stdout
            elif stderr:
                current_python_version = stderr
            else:
                raise Exception("Can't determine Python version")

            self.python_version = current_python_version.split()[1]

            if "anaconda" in current_python_version.lower():
                self.conda = True
                self.virtualenv = False
            else:
                self.conda = False
                if hasattr(sys, "real_prefix") or (
                    hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
                ):
                    self.virtualenv = True
                else:
                    self.virtualenv = False

        system_python_options = [
            "/usr/bin/python3.7",
            "/usr/bin/python3.6",
            "/usr/bin/python3.5",
            "/usr/bin/python3",
            "/usr/bin/python2.7",
            "/usr/bin/python2",
        ]
        self.system_python = None
        for p in system_python_options:
            if os.path.exists(p):
                if self.check_python_works(p):
                    self.system_python = p
                    break

        if self.system_python is None:
            self.system_python = find_executable("python3")

        if self.system_python is not None:
            works = self.check_python_works(self.system_python)
            if not works:
                self.system_python = None

        if self.system_python is None:

            pyenv_python_path = os.path.realpath(
                os.path.expanduser("~/.pyenv/shims/python3")
            )
            if os.path.exists(pyenv_python_path):
                works = self.check_python_works(pyenv_python_path)
                if works:
                    self.system_python = pyenv_python_path

            if self.system_python is None:
                exe = find_executable("python")
                works = self.check_python_works(exe)
                if works:
                    self.system_python = exe

            if self.system_python is None:
                pyenv_python_path = os.path.realpath(
                    os.path.expanduser("~/.pyenv/shims/python")
                )
                if os.path.exists(pyenv_python_path):
                    works = self.check_python_works(pyenv_python_path)
                    if works:
                        self.system_python = pyenv_python_path

        if self.system_python:
            system_python = local[self.system_python]
            rc, stdout, stderr = system_python.run("--version")
            if stdout:
                system_python_version = stdout
            elif stderr:
                system_python_version = stderr
            else:
                raise Exception("Can't determine Python version")

            self.system_python_version = system_python_version.split()[1]
        else:
            self.system_python_version = None

    def check_python_works(self, python_exe_path):

        p = local[python_exe_path]
        works = False
        try:
            rc, stdout, stderr = p.run(["--version"])
            works = rc == 0
            if not works:
                log.debug(
                    "Can't use python '{}', probably pyenv shim...".format(
                        python_exe_path
                    )
                )
                return False
        except (Exception) as e:
            log.debug("Can't use python '{}': {}".format(python_exe_path, e))
            return False

        try:
            rc, stdout, stderr = p.run(["-c", "from distutils import util"])
            if rc != 0:
                log.debug("Can't use python '{}': No distutils found..")
                return False
        except (Exception) as e:
            log.debug("Can't use python '{}': {}".format(python_exe_path, e))
            return False

        try:
            rc, stdout, stderr = p.run(["-c", "import ensurepip"])
            if rc == 0:
                log.debug(
                    "System python '{}' has venv and ensurepip modules, using virtualenv.".format(
                        python_exe_path
                    )
                )
                return True
        except (Exception) as e:
            log.debug("Can't use python '{}': {}".format(python_exe_path, e))

        return False

    def lookup_paths(self, incl_system_path=True, include_frozen=True):

        if incl_system_path:
            result = self._lookup_paths + [os.environ["PATH"]]
        else:
            result = self._lookup_paths

        if include_frozen:
            result = result + self._lookup_path_frozen

        return result

    def lookup_paths_string(self, incl_system_paths=True):

        return ":".join(self.lookup_paths(incl_system_path=incl_system_paths))

    def execute_external_comand(self, command, args=None, parent_task=None):

        env = dict(os.environ)  # make a copy of the environment
        lp_key = "LD_LIBRARY_PATH"  # for Linux and *BSD.
        lp_orig = env.get(lp_key + "_ORIG")  # pyinstaller >= 20160820 has this

        with local.env():

            if lp_orig is not None:
                local.env[lp_key] = lp_orig  # restore the original, unmodified value
            else:
                local.env.pop(lp_key, None)  # last resort: remove the env var

            cmd = local[command]
            if args is not None:
                rc, stdout, stderr = cmd.run(args)
            else:
                rc, stdout, stderr = cmd.run()

        return (rc, stdout, stderr)

    def ensure_python_packages(
        self,
        package_list,
        allow_current=False,
        venv_path=None,
        conda_path=None,
        conda_install_path=DEFAULT_CONDA_INSTALL_PATH,
        env_type=None,
        parent_task=None,
        system_site_packages=False,  # only applicable for virtualenv
    ):

        if parent_task is None:
            parent_task = DummyTaskDetail()

        if venv_path is not None and not os.path.isabs(os.path.expanduser(venv_path)):
            raise Exception("'venv_path' needs to be absolute")

        if allow_current and (self.virtualenv or self.conda):

            # TODO: check if available in other envs
            install_task = parent_task.add_subtask(
                task_name="package install",
                msg="installing packages: {}".format(", ".join(package_list)),
                # msg="x"
            )
            installed = install_and_import(
                package_list=package_list, import_modules=False
            )
            if installed:
                changed = True
                skipped = False
            else:
                changed = False
                skipped = True
            install_task.finish(success=True, changed=changed, skipped=skipped)
            return

        if env_type is None or env_type == "auto":

            if venv_path is None and conda_path is not None:
                env_type = "conda"
                if not os.path.isabs(os.path.expanduser(conda_path)):
                    raise Exception("'conda_path' is not an absolute path")
                conda_path = os.path.realpath(os.path.expanduser(conda_path))
                if not os.path.isdir(conda_path):
                    raise Exception("'conda_path is not a directory")

            elif venv_path is not None and conda_path is None:
                env_type = "virtualenv"
                if not os.path.isabs(os.path.expanduser(venv_path)):
                    raise Exception("'venv_path' is not an absolute path")
                venv_path = os.path.realpath(os.path.expanduser(venv_path))
                if not os.path.isdir(venv_path):
                    raise Exception("'venv_path is not a directory")
            else:
                if conda_path is None:
                    conda_path_exists = False
                else:
                    if not os.path.isabs(os.path.expanduser(conda_path)):
                        raise Exception("'conda_path' is not an absolute path")
                    conda_path = os.path.realpath(os.path.expanduser(conda_path))

                    conda_path_exists = os.path.exists(conda_path)

                    if conda_path_exists and not os.path.isdir(conda_path):
                        raise Exception("'conda_path is not a directory")

                if venv_path is None:
                    venv_path_exists = False
                else:
                    if not os.path.isabs(os.path.expanduser(venv_path)):
                        raise Exception("'venv_path' is not an absolute path")
                    venv_path = os.path.realpath(os.path.expanduser(venv_path))

                    venv_path_exists = os.path.exists(venv_path)

                    if venv_path_exists and not os.path.isdir(venv_path):
                        raise Exception("'venv_path is not a directory")

                if venv_path_exists and conda_path_exists:
                    env_type = "auto"
                elif venv_path_exists and not conda_path_exists:
                    env_type = "virtualenv"
                elif not venv_path_exists and conda_path_exists:
                    env_type = "conda"
                else:
                    env_type = "auto"

        if env_type == "auto":
            log.debug(
                "Can't find existing conda nor virtualenv environments, auto-determining env type..."
            )
            env_type = self.determine_best_env_type(
                conda_install_path=conda_install_path, default="virtualenv"
            )

        if env_type == "conda":
            env_path = conda_path
        else:
            env_path = venv_path

        env_exists = os.path.exists(env_path)
        if not env_exists:

            try:
                if env_type == "conda":
                    self.create_conda_env(
                        env_path, conda_install_path, parent_task=parent_task
                    )
                else:
                    self.create_virtualenv(
                        env_path,
                        parent_task=parent_task,
                        system_site_packages=system_site_packages,
                    )

            except (Exception) as e:
                shutil.rmtree(env_path, ignore_errors=True)
                raise e

            pip_task = None
            try:
                pip_task = parent_task.add_subtask(
                    task_name="updating pip", msg="updating 'pip' package"
                )
                pip = local[os.path.join(env_path, "bin", "pip")]
                pip(["install", "-U", "pip"])
                # TODO check whether changed
                pip_task.finish(success=True, skipped=False, changed=True)
            except (Exception) as e:
                if pip_task is not None:
                    pip_task.finish(success=False, error_msg=str(e))
                raise e

        try:
            install_task = parent_task.add_subtask(
                task_name="install packages",
                msg="installing: {}".format(", ".join(package_list)),
            )
            pip = local[os.path.join(env_path, "bin", "pip")]
            pip_args = ["install"] + package_list
            pip(pip_args)
            # TODO: check whether changed
            install_task.finish(success=True, changed=True, skipped=False)
        except (Exception) as e:
            install_task.finish(success=False, error_msg=str(e))

    def determine_best_env_type(self, default="virtualenv", conda_install_path=None):

        if not self.system_python:
            log.debug("No system python found, using conda.")
            return "conda"
        else:

            # check whether distutils is available
            log.debug("Checking for existing distutils module.")
            sys_python = local[self.system_python]
            try:
                rc, stdout, stderr = sys_python.run(
                    ["-c", "from distutils import util"]
                )
                if rc != 0:
                    log.debug("No distutils found, using conda.")
                    return "conda"
                else:
                    log.debug("Distutils found.")
            except (Exception):
                log.debug("No distutils found, using conda.")
                return "conda"

        lookup_path = self.lookup_paths_string()
        if conda_install_path:
            lookup_path = conda_install_path + ":" + lookup_path

        # check whether either conda or virtualenv commands exist
        conda_exe_path = find_executable("conda", path=lookup_path)
        virtualenv_exe_path = find_executable(
            "virtualenv", path=self.lookup_paths_string()
        )

        if conda_exe_path and not virtualenv_exe_path:
            log.debug("Conda found, but not virtualenv, using conda.")
            return "conda"
        elif not conda_exe_path and virtualenv_exe_path:
            log.debug("virtualenv found, but not conda, using virtualenv.")
            return "virtualenv"

        # check whether system python supports venv module
        sys_python = local[self.system_python]
        try:
            rc, stdout, stderr = sys_python.run(["-c", "import venv"])
            if rc == 0:
                rc, stdout, stderr = sys_python.run(["-c", "import ensurepip"])
                if rc == 0:
                    log.debug(
                        "System python has venv and ensurepip modules, using virtualenv."
                    )
                    return "virtualenv"
        except (Exception):
            pass

        log.debug("Using default env: {}".format(default))

        return default

    def create_virtualenv(self, path, parent_task, system_site_packages=False):

        # m = "preparing virtualenv: {}".format(path)
        # venv_task = parent_task.add_subtask(task_name="env create",
        #                                            msg=m)

        # TODO: check whether system python exists

        create_virtualenv(
            path=path,
            python_exe=self.system_python,
            parent_task=parent_task,
            lookup_paths_string=self.lookup_paths_string(),
            system_site_packages=system_site_packages,
        )

    def create_conda_env(
        self, path, conda_path=DEFAULT_CONDA_INSTALL_PATH, parent_task=None
    ):

        if parent_task is None:
            parent_task = DummyTaskDetail()

        # TODO: check whether conda exe exists somewhere else

        if not os.path.exists(os.path.join(conda_path, "bin", "activate")):
            install_miniconda(path=conda_path, parent_task=parent_task)

        if not os.path.exists(os.path.join(path, "bin", "pip")):
            with parent_task.subtask(
                task_name="create conda env",
                msg="creating conda environment: {}".format(path),
            ) as task:

                conda = local[os.path.join(conda_path, "bin", "conda")]
                rc, stdout, stderr = conda.run(["create", "-y", "-p", path])
                task.msg = stdout
                task.error_msg = stderr

            with parent_task.subtask(
                task_name="installing base packages",
                msg="installing base packages: python, pip",
            ) as task:

                conda = local[os.path.join(conda_path, "bin", "conda")]
                rc, stdout, stderr = conda.run(
                    ["install", "-p", path, "-y", "python==3.6", "pip"]
                )
                task.msg = stdout
                task.error_msg = stderr

    # def inaugurate_conda_env(self, path, parent_task):
    #
    #     inaugurate_script_content = generate_inaugurate_script()
    #
    #     bash = local["bash"]
    #
    #     read, write = os.pipe()
    #     os.write(write, inaugurate_script_content.encode())
    #     os.close(write)
    #
    #     try:
    #         with local.env(
    #             NO_EXEC="true",
    #             NO_ADD_PATH="true",
    #             FORCE_INAUGURATE="true",
    #             CHINA="falseF",
    #         ):
    #             bash.run(
    #                 ["-s", "--"], stdin=read, stdout=sys.stdout, stderr=sys.stderr
    #             )
    #     except (Exception) as e:
    #         log.error(e, exc_info=1)
    #     finally:
    #         sys.exit(1)

    # def ensure_pip(self):
    #
    #     pip = local["pip"]
    #
    #     if pip is not None:
    #         return
    #
    #     url = "https://bootstrap.pypa.io/get-pip.py"
    #     r = requests.get(url, allow_redirects=True)
    #     temp_file = NamedTemporaryFile()
    #     with io.open(temp_file.name, "wb", encoding="utf-8") as f:
    #         f.write(r.content)


def install_and_import(package_list, import_modules=False):
    import importlib

    if isinstance(package_list, string_types):
        package_list = [package_list]

    to_install = []

    for package in package_list:

        try:
            importlib.import_module(package)
        except ImportError:
            to_install.append(package)

    if not to_install:
        return []
    try:
        sys_python = local[sys.executable]

        sys_python(["-m", "pip", "install"] + to_install)
        # print(rc)
        # print(stdout)
        # print(stderr)
        # out = subprocess.check_output(  # nosec
        #     [sys.executable, "-m", "pip", "install"] + to_install
        # )
        # print(stdout)
        # log.debug("pip output: {}".format(stdout))
        return to_install
    except (subprocess.CalledProcessError) as e:
        print("Failed to install '{}': {}".format(to_install, e.output))
        sys.exit(e.returncode)
    finally:
        if import_modules:
            for package in to_install:
                globals()[package] = importlib.import_module(package)
