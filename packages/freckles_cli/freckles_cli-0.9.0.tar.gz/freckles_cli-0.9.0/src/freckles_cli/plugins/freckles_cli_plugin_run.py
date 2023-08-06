from __future__ import absolute_import, division, print_function

import logging

import click
from ruamel.yaml import YAML

from frkl import VarsType

yaml = YAML(typ="safe")

log = logging.getLogger("freckles")

TEST_INVENTORY = {
    "target": "localhost",
    "gid": 3000,
    "group": "testgroup",
    "system_user": False,
    "name": "Markus",
    "path": "/tmp/markus",
}


@click.command()
@click.option("--vars", "-v", help="vars for frecklet", multiple=True, type=VarsType())
@click.argument("frecklet_data", required=False, metavar="FRECKLET_DATA", nargs=-1)
@click.pass_context
def run(ctx, vars, frecklet_data):
    """
    Run, inspect or debug a frecklet
    """

    pass

    # if not frecklet_data:
    #     frecklet_data = []
    #
    #     stream = click.get_text_stream("stdin", encoding="utf-8")
    #
    #     for line in stream:
    #         frecklet_data.append(line)
    #
    #     frecklet_data = "".join(frecklet_data)
    #     frecklet_data = [frecklet_data]

    # context = ctx.obj["context"]
    #
    # all_vars = {}
    # for v in vars:
    #     dict_merge(all_vars, v, copy_dct=False)
    #
    # run_config = ctx.obj["run_config"]
    #
    # frecklets = []
    #
    # for fd in frecklet_data:
    #
    #     if fd in context.get_frecklet_names():
    #         frecklets.append(fd)
    #
    # import pp
    # pp(frecklets)

    # run_frecklet(
    #     ctx=ctx,
    #     frecklet_name=frecklet,
    #     freckles_context=freckles_context,
    #     run_config=run_config,
    #     vars=all_vars,
    # )
