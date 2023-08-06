# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import click

from frkl import VarsType


# from . import __version__ as VERSION


@click.group("inaugurate")
@click.pass_context
def inaugurate(ctx):
    """Manage 'inaugurate' scripts"""

    pass


@inaugurate.command("generate")
@click.argument(
    "metadata", metavar="METADATA", required=False, type=VarsType(), nargs=-1
)
@click.pass_context
def generate(ctx, metadata=None):
    """Generate a customized 'inaugurate' script.
    """

    pass
