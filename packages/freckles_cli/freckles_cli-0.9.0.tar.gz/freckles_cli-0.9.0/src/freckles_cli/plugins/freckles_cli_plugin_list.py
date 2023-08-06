from __future__ import absolute_import, division, print_function

import logging
import sys
from collections import OrderedDict

import click
from ruamel.yaml import YAML

from freckles.utils.utils import print_frecklet_list

yaml = YAML(typ="safe")

log = logging.getLogger("freckles")


@click.command()
@click.option(
    "--filter",
    "-f",
    help="filter frecklets with specified string in them",
    type=str,
    multiple=True,
)
@click.pass_context
def list(ctx, filter):
    """
    List available frecklets and their details.
    """

    context = ctx.obj["context"]

    apropos = filter
    check_doc = False

    result = OrderedDict()
    for f_name, f in context.frecklet_index.items():
        match = True
        for a in apropos:
            if a not in f_name:
                match = False
                break

        if match:
            result[f_name] = f
            continue

        if check_doc:
            match = f.doc.matches_apropos(apropos, only_short_help=True)
        else:
            match = False

        if match:
            result[f_name] = f

    print_frecklet_list(result)

    sys.exit(0)
