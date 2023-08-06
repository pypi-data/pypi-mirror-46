# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click

from frkl import VarsType
from frkl_pkg import FrklPkg


# from . import __version__ as VERSION


@click.group("pkg")
@click.pass_context
def pkg(ctx):
    """Manage 'inaugurate' scripts"""

    pass


@pkg.command("install_conda")
@click.argument(
    "metadata", metavar="METADATA", required=False, type=VarsType(), nargs=-1
)
@click.pass_context
def install_conda(ctx, metadata=None):
    """Generate a customized 'inaugurate' script.
    """

    frkl_pkg = FrklPkg()

    frkl_pkg.create_conda_env("/tmp/test")
