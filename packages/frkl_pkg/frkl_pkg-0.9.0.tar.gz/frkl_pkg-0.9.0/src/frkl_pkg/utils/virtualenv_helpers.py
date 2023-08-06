# -*- coding: utf-8 -*-
import io
import logging
import os
import tempfile
from distutils.spawn import find_executable

import requests
from plumbum import local

from frkl_pkg.defaults import (
    PIP_WHEEL_DOWNLOAD_URL,
    VIRTUALENV_WHEEL_DOWNLOAD_URL,
    LOOKUP_PATHS_STRING,
)

log = logging.getLogger("frkl_pkg")


def create_virtualenv(
    path,
    python_exe,
    parent_task,
    lookup_paths_string=LOOKUP_PATHS_STRING,
    prefer_no_deps=True,
    system_site_packages=False,
):
    """Create a Python virtualenv.

    Args:
        path: the path of the virtualenv
        python_exe: the path to the python executable to use
        parent_task: the parent task
        prefer_no_deps: use the 'no_deps' install method if everything else fails

    Returns:

    """
    python_cmd = local[python_exe]
    venv_command = None
    try:
        rc, stdout, stderr = python_cmd.run(["-c", "import venv"])
        if rc == 0:
            rc, stdout, stderr = python_cmd.run(["-c", "import ensurepip"])
            if rc == 0:
                if system_site_packages:
                    venv_command = python_cmd.bound_command(
                        "-m", "venv", "--system-site-packages", path
                    )
                else:
                    venv_command = python_cmd.bound_command("-m", "venv", path)
    except (Exception):
        pass

    if venv_command is None:
        virtualenv_exe = find_executable("virtualenv")
        if virtualenv_exe:
            if system_site_packages:
                venv_command = local[virtualenv_exe].bound_command(
                    "--system-site-packages", path
                )
            else:
                venv_command = local[virtualenv_exe].bound_command(path)

    if venv_command is not None:
        current = parent_task.add_subtask(
            task_name="creating virtualenv",
            msg="creating virtualenv in: {}".format(path),
        )
        venv_command()
        current.finish(success=True, skipped=False, changed=True)
        return

    if prefer_no_deps:

        create_virtualenv_no_deps(
            path=path,
            python_exe=python_exe,
            parent_task=parent_task,
            system_site_packages=system_site_packages,
        )

    else:
        install_virtualenv_user(
            python=python_exe,
            parent_task=parent_task,
            lookup_paths_string=lookup_paths_string,
        )
        virtualenv_exe = find_executable("virtualenv", path=lookup_paths_string)
        if system_site_packages:
            venv_command = local[virtualenv_exe].bound_command(
                "--system-site-packages", path
            )
        else:
            venv_command = local[virtualenv_exe].bound_command(path)
        current = parent_task.add_subtask(
            task_name="creating virtualenv",
            msg="creating virtualenv in: {}".format(path),
        )
        venv_command()
        current.finish(success=True, skipped=False, changed=True)


def create_virtualenv_no_deps(
    path, python_exe, parent_task, system_site_packages=False
):

    with tempfile.TemporaryDirectory() as tmpdirname:
        pip_path = os.path.join(tmpdirname, "pip.zip")
        virtualenv_path = os.path.join(tmpdirname, "virtualenv.zip")
        current = parent_task.add_subtask(
            task_name="downloading pip", msg="downloading pip"
        )
        try:
            req = requests.get(PIP_WHEEL_DOWNLOAD_URL, allow_redirects=True)
            with io.open(pip_path, "wb") as f:
                f.write(req.content)
        except (Exception) as e:
            current.finish(success=False, error_msg=str(e))
            raise Exception("Could not download pip: {}".format(e))
        current.finish(success=True, changed=True, skipped=False)

        current = parent_task.add_subtask(
            task_name="downloading virtualenv", msg="downloading virtualenv"
        )
        try:
            req = requests.get(VIRTUALENV_WHEEL_DOWNLOAD_URL, allow_redirects=True)
            with io.open(virtualenv_path, "wb") as f:
                f.write(req.content)
        except (Exception) as e:
            current.finish(success=False, error_msg=str(e))
            raise Exception("Could not download pip: {}".format(e))
        current.finish(success=True, changed=True, skipped=False)

        current = parent_task.add_subtask(
            task_name="creating virtualenv",
            msg="creating virtualenv in: {}".format(path),
        )
        script_path = os.path.join(tmpdirname, "create_virtualenv.py")
        script_content = """import runpy
runpy.run_module('virtualenv', run_name='__main__', alter_sys=True)
"""
        with io.open(script_path, "w") as f:
            f.write(script_content)

        with local.env(PYTHONPATH="{}:{}".format(pip_path, virtualenv_path)):

            python_cmd = local[python_exe]
            if system_site_packages:
                rc, stdout, stderr = python_cmd.run(
                    [script_path, "--system-site-packages", path]
                )
            else:
                rc, stdout, stderr = python_cmd.run([script_path, path])

            success = rc == 0
            current.finish(
                success=success,
                skipped=False,
                changed=True,
                msg=stdout,
                error_msg=stderr,
            )


def install_virtualenv_user(
    python_exe, parent_task, lookup_paths_string=LOOKUP_PATHS_STRING
):

    python_cmd = local[python_exe]
    # check whether pip is available
    pip_exe = find_executable("pip3", path=lookup_paths_string)
    if not pip_exe:
        pip_exe = find_executable("pip", path=lookup_paths_string)
    if not pip_exe:
        current = parent_task.add_subtask(
            task_name="create tempdir", msg="creating temporary directory"
        )
        with tempfile.TemporaryDirectory() as tmpdirname:
            current.finish(success=True, changed=True, skipped=False)
            get_pip_file_path = os.path.join(tmpdirname, "get-pip.py")
            url = "https://bootstrap.pypa.io/get-pip.py"
            current = parent_task.add_subtask(
                task_name="downloading pip", msg="downloading pip from: {}".format(url)
            )
            try:
                req = requests.get(url, allow_redirects=True)
                with io.open(get_pip_file_path, "wb") as f:
                    f.write(req.content)
            except (Exception) as e:
                current.finish(success=False, error_msg=str(e))
                raise Exception("Could not download pip: {}".format(e))

            current.finish(success=True, changed=True, skipped=False)

            current = parent_task.add_subtask(
                task_name="install pip",
                msg="installing 'pip' package (into $HOME/.local/bin)",
            )
            try:
                rc, stdout, stderr = python_cmd.run(
                    [get_pip_file_path, "--user", "--no-setuptools", "--no-wheel"]
                )
            except (Exception) as e:
                current.finish(success=False, error_msg=str(e))
                raise Exception("Could not install 'pip': {}".format(stderr))

            if rc == 0:
                current.finish(
                    success=True,
                    changed=True,
                    skipped=False,
                    msg=stdout,
                    error_msg=stderr,
                )
            else:
                current.finish(success=False, msg=stdout, error_msg=stderr)
                raise Exception("Could not install 'pip': {}".format(stderr))

        pip_exe = find_executable("pip", path=lookup_paths_string)

    current = parent_task.add_subtask(
        task_name="install virtualenv",
        msg="installing 'virtualenv' package (into $HOME/.local/bin)",
    )
    # TODO: error handling
    pip = local[pip_exe]
    pip("install", "--user", "virtualenv")
    current.finish(success=True, changed=True, skipped=False)
