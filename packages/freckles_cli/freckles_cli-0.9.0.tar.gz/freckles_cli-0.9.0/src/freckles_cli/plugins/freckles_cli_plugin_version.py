# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging
import sys

import click
from ruamel.yaml import YAML

from freckles.utils.versions import get_versions

yaml = YAML(typ="safe")

log = logging.getLogger("freckles")


@click.command()
@click.option(
    "--all",
    "-a",
    help="display version information for all (frkl-) project dependencies",
    is_flag=True,
)
@click.pass_context
def version(ctx, all):
    """
    Display freckles version information
    """

    versions = get_versions()

    if all:
        for k, v in versions.items():
            print("{}: {}".format(k, v))
        sys.exit()

    from freckles import __version__

    print(__version__)
