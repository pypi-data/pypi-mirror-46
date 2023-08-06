# -*- coding: utf-8 -*-
import io
import logging
import os
import platform
import tempfile

import requests
from plumbum import local

from frutils.tasks.tasks import DummyTaskDetail

log = logging.getLogger("frkl_pkg")


def calculate_platform():

    uname_info = platform.uname()
    return {"os": uname_info[0], "arch": uname_info[4]}


def install_miniconda(path, parent_task=None):

    if parent_task is None:
        parent_task = DummyTaskDetail()

    platform_info = calculate_platform()

    url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-{}-{}.sh".format(
        platform_info["os"], platform_info["arch"]
    )

    current = parent_task.add_subtask(
        task_name="create tempdir", msg="creating temporary directory"
    )
    # download conda
    with tempfile.TemporaryDirectory() as tmpdirname:

        current.finish(success=True, changed=True, skipped=False)

        conda_installer_path = os.path.join(tmpdirname, "miniconda.sh")

        with parent_task.subtask(
            task_name="downloading miniconda",
            msg="downloading miniconda from: {}".format(url),
        ):
            req = requests.get(url, allow_redirects=True)
            with io.open(conda_installer_path, "wb") as f:
                f.write(req.content)

        with parent_task.subtask(
            task_name="installing miniconda",
            msg="installing miniconda to: {}".format(path),
        ):

            sh = local["sh"]
            sh([conda_installer_path, "-b", "-p", path])
