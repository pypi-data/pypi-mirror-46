# -*- coding: utf-8 -*-
import os

DEFAULT_CONDA_INSTALL_PATH = os.path.expanduser("~/miniconda3")
NON_VENV_PYTHON_VERSIONS = ["1", "2", "3.0", "3.1", "3.2"]

LOOKUP_PATHS = [
    os.path.expanduser("~/.local/bin"),
    os.path.join(DEFAULT_CONDA_INSTALL_PATH, "bin"),
    os.path.expanduser("~/Library/Python/2.7/bin"),
]


LOOKUP_PATHS_STRING = ":".join(LOOKUP_PATHS)


PIP_WHEEL_DOWNLOAD_URL = "https://files.pythonhosted.org/packages/d8/f3/413bab4ff08e1fc4828dfc59996d721917df8e8583ea85385d51125dceff/pip-19.0.3-py2.py3-none-any.whl"
VIRTUALENV_WHEEL_DOWNLOAD_URL = "https://files.pythonhosted.org/packages/33/5d/314c760d4204f64e4a968275182b7751bd5c3249094757b39ba987dcfb5a/virtualenv-16.4.3-py2.py3-none-any.whl"
