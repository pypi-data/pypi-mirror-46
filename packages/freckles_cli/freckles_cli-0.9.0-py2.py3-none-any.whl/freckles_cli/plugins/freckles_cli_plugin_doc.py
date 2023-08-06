from __future__ import absolute_import, division, print_function

import logging

import click
import mdv
from ruamel.yaml import YAML

from frutils import get_terminal_size

yaml = YAML(typ="safe")

log = logging.getLogger("freckles")


@click.command()
@click.argument("frecklet", nargs=1, required=True, metavar="FRECKLET_NAME")
@click.pass_context
def doc(ctx, frecklet):
    """
    Display the documentation for a frecklet.
    """

    context = ctx.obj["context"]

    f, internal_name = context.load_frecklet(frecklet)

    mdv.term_columns = get_terminal_size()[0] - 10

    rendered = mdv.main(f.markdown, no_colors=True)

    click.echo(rendered.encode("utf-8"))
