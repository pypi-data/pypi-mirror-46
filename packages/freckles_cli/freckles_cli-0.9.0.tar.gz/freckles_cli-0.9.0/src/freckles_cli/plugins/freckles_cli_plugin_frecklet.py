# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging
import sys
from collections import OrderedDict

import click
from ruamel.yaml import YAML

from freckles.defaults import FRECKLET_KEY_NAME
from freckles.frecklet.describe import (
    create_auto_vars,
    describe_frecklet,
    print_task_descriptions,
)
from freckles.frecklet.vars import VarsInventory
from freckles.utils.utils import print_multi_column_table
from freckles_cli.freckles_base_cli import handle_exception
from frkl import VarsType
from frutils import dict_merge, readable_yaml, reindent
from frutils.frutils_cli import output

yaml = YAML(typ="safe")

log = logging.getLogger("freckles")


@click.group(name="frecklet")
# @click.argument("frecklet", nargs=1, required=True, metavar="FRECKLET_NAME")
@click.pass_context
def frecklet(ctx):
    """
    Run, inspect or debug a frecklet
    """

    # ctx.obj["frecklet_name"] = frecklet
    pass


@frecklet.command("task-tree")
@click.argument("frecklet_name", nargs=1)
@click.pass_context
def task_tree(ctx, frecklet_name):
    """Print the execution plan for a frecklet.

    Print out a hierarchical tree-structure, containing all tasks that will be executed, including their parents.
    """

    context = ctx.obj["context"]

    f, internal_name = context.load_frecklet(frecklet_name)
    click.echo()
    click.echo(
        "{} ({}):".format(frecklet_name, f.doc.get_short_help(list_item_format=True))
    )

    for n in f.task_tree.all_nodes():
        level = f.task_tree.level(n.identifier)
        if level == 0:
            continue
        padding = "  " * level
        # print(n.data["task"].keys())
        task = n.data["task"]
        name = task[FRECKLET_KEY_NAME]["name"]
        # import pp
        # pp(task)
        f_type = task[FRECKLET_KEY_NAME].get("type", "frecklet")
        short_help = ""
        if f_type == "frecklet":
            short_help = context.get_frecklet(name).doc.get_short_help(
                list_item_format=True
            )
            # short_help = task[FRECKLET_KEY_NAME].get("msg", None)
            title = "{} ({})".format(name, short_help)

        else:
            title = "{}::{}".format(f_type, name)
        print("{}- {}".format(padding, title))


@frecklet.command("task-list")
@click.argument("frecklet_name", type=str, nargs=1)
@click.argument("vars", type=VarsType(), nargs=-1)
@click.option(
    "--auto-vars",
    "-a",
    help="auto generate missing required variables",
    required=False,
    is_flag=True,
)
@click.pass_context
def task_list(ctx, frecklet_name, vars, auto_vars):
    """Print the rendered tasklist for a frecklet.

    Render and process the frecklet task-list using the provided vars, display the output in human-readable form.

    """

    context = ctx.obj["context"]

    frecklet, internal_name = context.load_frecklet(frecklet_name)
    fx = frecklet.create_frecklecutable(context=context)

    var_all = {}

    for v in vars:
        dict_merge(var_all, v, copy_dct=False)

    if auto_vars:
        params = fx.frecklet.vars_frecklet
        auto_vars = create_auto_vars(
            params, existing_vars=var_all, frecklet=fx.frecklet
        )
        click.echo("\n----------------------------------------------")
        click.echo("Auto-generated (missing) required variables:\n")
        output(auto_vars, output_type="yaml", indent=2)
        click.echo("----------------------------------------------\n")

        var_all = dict_merge(auto_vars, var_all, copy_dct=True)

    inv = VarsInventory(var_all)
    tasks = fx.process_tasks(inventory=inv)

    tl_string = readable_yaml(tasks, ignore_aliases=True)
    click.echo(tl_string)


@frecklet.command("print")
@click.argument("frecklet_name", type=str, nargs=1)
@click.pass_context
def print_frecklet(ctx, frecklet_name):
    """Print the raw frecklet content."""

    context = ctx.obj["context"]
    frecklet, internal_name = context.load_frecklet(frecklet_name)

    if not frecklet:
        click.echo("No frecklet with name: {}".format(frecklet_name))
        sys.exit(1)

    for key in ["doc", "args", "meta", "frecklets"]:
        if frecklet._metadata.get(key, None):
            click.echo("{}:".format(key))
            result = readable_yaml(
                frecklet._metadata[key], sort_keys=True, ignore_aliases=True
            )
            click.echo(reindent(result, 2))


@frecklet.command("args")
@click.option(
    "--full", "-f", is_flag=True, help="Print the full description for every argument."
)
@click.argument("frecklet_name", type=str, nargs=1)
@click.pass_context
def args(ctx, frecklet_name, full, raw=False, sort_by_name=False):
    """Print the arguments of the frecklets."""

    context = ctx.obj["context"]
    frecklet, internal_name = context.load_frecklet(frecklet_name)

    if not frecklet:
        click.echo("No frecklet with name: {}".format(frecklet_name))
        sys.exit(1)

    try:

        if raw:

            if frecklet._metadata.get("args", None):
                click.echo("{}:".format("args"))
                result = readable_yaml(
                    frecklet._metadata["args"], sort_keys=True, ignore_aliases=True
                )
                click.echo(reindent(result, 2))

        else:

            if full:
                result = OrderedDict()
                if sort_by_name:
                    for k, arg in frecklet.vars_frecklet.items():
                        details = arg.pretty_print_dict()
                        result[k] = details
                else:
                    for k, arg in frecklet.vars_frecklet.items():
                        if arg.required is True:
                            details = arg.pretty_print_dict()
                            result[k] = details
                    for k, arg in frecklet.vars_frecklet.items():
                        if arg.required is False:
                            details = arg.pretty_print_dict()
                            result[k] = details

                click.echo()

                for k, v in result.items():
                    click.secho(k, bold=True)
                    click.echo()
                    details = readable_yaml(v, indent=2, ignore_aliases=True)
                    click.echo(details)

            else:

                data = OrderedDict()
                if sort_by_name:
                    for k, arg in frecklet.vars_frecklet.items():
                        data[k] = arg
                else:
                    for k, arg in frecklet.vars_frecklet.items():
                        if arg.required is True:
                            data[k] = arg
                    for k, arg in frecklet.vars_frecklet.items():
                        if arg.required is False:
                            data[k] = arg

                result = []
                for k, arg in data.items():
                    if arg.required:
                        arg_req = "X"
                    else:
                        arg_req = ""

                    desc = arg.doc.get_short_help(list_item_format=True, use_help=True)
                    arg_type = arg.type
                    if arg.default is not None:
                        arg_default = arg.default
                    else:
                        arg_default = ""
                    result.append([k, arg_type, arg_req, arg_default, desc])

                click.echo()

                print_multi_column_table(
                    result, ["arg", "type", "req", "default", "desc"]
                )
    except (Exception) as e:
        handle_exception(e)


@frecklet.command("describe")
@click.argument("frecklet_name", type=str, nargs=1)
@click.argument("vars", type=VarsType(), nargs=-1)
@click.option(
    "--auto-vars",
    "-a",
    help="auto generate missing required variables",
    required=False,
    is_flag=True,
)
@click.pass_context
def describe(ctx, frecklet_name, vars, auto_vars):
    """Print the rendered tasklist for a frecklet.

    Render and process the frecklet task-list using the provided vars, display the output in human-readable form.

    """

    context = ctx.obj["context"]

    frecklet, _ = context.load_frecklet(frecklet_name)
    tasks_descs, auto_vars_dict = describe_frecklet(
        context=context, frecklet=frecklet, vars=vars, auto_vars=auto_vars
    )

    if auto_vars_dict:
        click.echo("\n----------------------------------------------")
        click.echo("Auto-generated (missing) required variables:\n")
        output(auto_vars_dict, output_type="yaml", indent=2)
        click.echo("----------------------------------------------\n")

    print_task_descriptions(tasks_descs)


@frecklet.command("explode")
@click.argument("frecklet_name", type=str, nargs=1)
@click.pass_context
def explode(ctx, frecklet_name, sort_by_name=False):

    context = ctx.obj["context"]

    frecklet, internal_name = context.load_frecklet(frecklet_name)
    if not frecklet:
        click.echo("No frecklet with name: {}".format(frecklet_name))
        sys.exit(1)

    result = frecklet.exploded

    click.echo()
    for k, v in result.items():
        click.secho(k, bold=True)
        click.echo()
        details = readable_yaml(v, indent=2, ignore_aliases=True)
        click.echo(details)
