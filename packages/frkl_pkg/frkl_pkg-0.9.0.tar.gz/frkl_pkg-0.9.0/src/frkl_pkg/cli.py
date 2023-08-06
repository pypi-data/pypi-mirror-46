# -*- coding: utf-8 -*-
"""Console script for frkl_pkg."""
import os
import sys

import click

# fix for pyinstaller & Python 2
if 0:
    pass


def cli(argv):
    """Console script for frkl_pkg."""

    # exe_path = os.path.dirname(argv[0])
    exe_name = os.path.basename(argv[0])

    exe_name_env = os.environ.get("f_ex", None)

    known_exes = ["freckles", "frecklecute"]

    if (
        exe_name_env is not None
        and (exe_name in known_exes)
        and (
            exe_name == "freckles.bin"
            or exe_name == "freckles"
            or exe_name == "frkl-pkg"
            or exe_name == "freckles-pkg"
            or exe_name == "freckles.pyz"
        )
    ):
        exe_name = exe_name_env

    args = argv[1:]

    if exe_name == "freckles":
        from freckles_cli.freckles_cli.freckles_cli import cli as freckles_cli

        freckles_cli(args)
    elif exe_name == "frecklecute":
        from freckles_cli.frecklecute.frecklecute_cli import cli as frecklecute_cli

        frecklecute_cli(args)

    else:

        click.echo(
            "No application registered for executable name '{}', doing nothing...".format(
                exe_name
            )
        )

    return 0


if __name__ == "__main__":
    sys.exit(cli(sys.argv))  # pragma: no cover


def main():
    sys.exit(cli(sys.argv))  # pragma: no cover


if getattr(sys, "frozen", False):
    cli(sys.argv)
