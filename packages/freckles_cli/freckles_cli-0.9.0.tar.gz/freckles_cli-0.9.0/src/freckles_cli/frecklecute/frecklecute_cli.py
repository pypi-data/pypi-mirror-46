# -*- coding: utf-8 -*-
from __future__ import print_function

import copy
import logging
import sys
from collections import OrderedDict, Sequence

import click
import click_completion
import click_log
from six import string_types

from freckles.frecklet.describe import describe_frecklet, print_task_descriptions
from freckles.utils.utils import print_frecklet_list
from freckles_cli.freckles_base_cli import (
    FrecklesBaseCommand,
    create_context,
    run_frecklet,
    handle_exception,
)
from frutils import dict_merge

log = logging.getLogger()
click_log.basic_config(log)

# optional shell completion
click_completion.init()

VARS_HELP = "variables to be used for templating, can be overridden by cli options if applicable"
DEFAULTS_HELP = "default variables, can be used instead (or in addition) to user input via command-line parameters"
KEEP_METADATA_HELP = "keep metadata in result directory, mostly useful for debugging"
FRECKLECUTE_EPILOG_TEXT = "frecklecute is part of the 'freckles' project. It is free to use in combination with open source software. For more information on licensing and documentation please visit: https://freckles.io"


def help_all(ctx, param, value):

    if ctx.obj is None:
        ctx.obj = {}

    # allowed_tags = ["__all__"]
    # ctx.obj["allowed_frecklet_tags"] = allowed_tags

    ctx.obj["ignore_frecklet_tags"] = ["impl", "ignore"]

    if value:

        freckles = create_context(ctx, force=True)

        print_frecklet_list(freckles.frecklets)

        sys.exit(0)


def help_only(ctx, param, value):

    if ctx.obj is None:
        ctx.obj = {}

    ctx.obj["help_only"] = True

    if value:
        ctx.obj["skip_frecklet_parsing"] = True
        command = ctx.command

        # create_context(ctx, force=True)

        help = command.get_help(ctx)
        click.echo(help)
        sys.exit(0)


def apropos(ctx, param, value):

    if ctx.obj is None:
        ctx.obj = {}

    if not value:
        apropos = None
    else:
        apropos = value

    if value:

        check_doc = True

        freckles = create_context(ctx, force=True)
        result = OrderedDict()
        for f_name, f in freckles.frecklets.items():
            match = True
            for a in apropos:
                if a not in f_name:
                    match = False
                    break

            if match:
                result[f_name] = f
                continue
            else:
                match = False

            try:
                if check_doc:
                    match = f.doc.matches_apropos(apropos, only_short_help=True)
                else:
                    match = False
            except (Exception) as e:
                log.warning(e)

            if match:
                result[f_name] = f

        print_frecklet_list(result)

        sys.exit(0)


class FrecklecuteCommand(FrecklesBaseCommand):
    def __init__(self, *args, **kwargs):
        super(FrecklecuteCommand, self).__init__(**kwargs)

    def list_freckles_commands(self, ctx):

        try:
            result = self.context.get_frecklet_names()
            # filter = ctx.obj["frecklet_filters"]
            filters = ctx.obj.get("frecklet_filters", None)

            if not filters:
                return sorted(result)

            filtered = []
            for f in result:
                match = True
                for filter in filters:
                    if filter.lower() not in f.lower():
                        match = False
                        break
                if match:
                    filtered.append(f)

            return sorted(filtered)
        except (Exception) as e:
            log.debug(e, exc_info=1)
            log.warning("Error creating commands: {}".format(e))
            sys.exit(1)

    def create_alias_map(self, arg_map):

        alias_map = {}
        for arg_name, arg in arg_map.items():

            if "param_decls" not in arg.get("cli", {}).keys():
                continue

            for a in arg["cli"]["param_decls"]:
                if a == arg_name:
                    continue
                if a in alias_map.keys():
                    raise Exception(self, "Duplicate alias/key: {}".format(a))
                if "/" in a:
                    a = a.split("/")[0]
                a = a.strip("-")
                a = a.replace("-", "_")
                alias_map[a] = arg_name

        return alias_map

    def remove_empty_lists(self, cli_vars, vars_frecklet):

        result = {}

        for k, v in cli_vars.items():
            if not v and not isinstance(v, string_types) and isinstance(v, Sequence):
                arg = vars_frecklet[k]
                required = arg.required

                if required:
                    result[k] = v
            else:
                result[k] = v

        return result

    def translate_cli_args(self, cli_vars, arg_map):

        alias_map = self.create_alias_map(arg_map)

        result = {}

        for key, value in cli_vars.items():
            if value is None:
                continue

            if key in alias_map.keys():
                result[alias_map[key]] = value
            else:
                result[key] = value

        return result

    def augment_default_values(self, extra_vars, cli_parameters, arg_map):

        alias_map = self.create_alias_map(arg_map)

        for param in cli_parameters:

            name = param.name
            if name in alias_map.keys():
                name = alias_map[name]

            if name not in extra_vars.keys() or extra_vars[name] is None:
                continue

            param.default = extra_vars[name]
            # param.required = False

        return cli_parameters

    def get_freckles_command(self, ctx, name):

        skip = ctx.obj.get("skip_frecklet_parsing", False)

        try:
            frecklet, frecklet_name = self.context.load_frecklet(name, validate=True)
        except (Exception) as e:
            handle_exception(e)

        try:

            @click.command(name=name)
            def command(*args, **kwargs):

                click.echo()

                user_input = self.remove_empty_lists(kwargs, frecklet.vars_frecklet)
                user_input = self.translate_cli_args(user_input, frecklet.args)
                vars = dict_merge(self.extra_vars, user_input, copy_dct=True)

                if ctx.params.get("describe", False):

                    click.echo()
                    click.secho(
                        "Tasklist for frecklet '{}' and the provided vars:".format(
                            name
                        ),
                        bold=True,
                    )
                    click.echo()

                    task_descs, _ = describe_frecklet(
                        context=self.context,
                        frecklet=frecklet,
                        vars=vars,
                        auto_vars=False,
                    )
                    print_task_descriptions(task_descs)
                    sys.exit()

                run_frecklet(
                    ctx=ctx,
                    frecklet=frecklet,
                    freckles_context=self.context,
                    run_config=self.run_config,
                    vars=vars,
                )

            try:
                # we don't want to process args if we only list all commands
                if not skip:
                    try:
                        cli_args = frecklet.cli_arguments
                        _parameters = copy.deepcopy(cli_args)
                        # setting default to extra var if appropriate
                        _parameters = self.augment_default_values(
                            self.extra_vars, _parameters, frecklet.args
                        )
                    except (Exception) as e:
                        # fe = FreckletException(
                        # frecklet=frecklet, parent_exception=e, frecklet_name=name
                        # )

                        handle_exception(e, frecklet=frecklet, frecklet_name=name)
                else:
                    _parameters = []

                command.params = _parameters
                command.help = frecklet.doc.get_help()
                command.short_help = frecklet.doc.get_short_help(list_item_format=True)
                # command.epilog = XXX

                return command
            except (Exception) as e:
                # parsing of frecklet failed
                handle_exception(e, frecklet=frecklet, frecklet_name=name)
                click.echo(e)
        except (Exception) as e:
            handle_exception(e, frecklet=frecklet, frecklet_name=name)


@click.command(
    name="frecklecute",
    cls=FrecklecuteCommand,
    epilog=FRECKLECUTE_EPILOG_TEXT,
    subcommand_metavar="FRECKLET [ARGS]",
)
# @click.option(
#     "--elevated", "-e",
#     help="indicate that this run needs elevated permissions",
#     flag_value="elevated",
#     required=False,
# )
# @click.option(
#     "--not-elevated", "-ne",
#     help="indicate that this run doesn't need elevated permissions",
#     flag_value="not_elevated",
#     required=False,
# )
@click.option(
    "--describe",
    help="Only describe tasks for this run, don't create an environment and run the frecklet.",
    is_flag=True,
)
@click.option(
    "--dump",
    help="Don't execute, only dump the resulting frecklet, including variables into stdout.",
    is_flag=True,
)
@click_log.simple_verbosity_option(logging.getLogger(), "--verbosity")
@click.option(
    "--apropos",
    "-a",
    help="Show this message, listing all commands that contain this value in their name or description.",
    metavar="WORD",
    type=str,
    multiple=True,
    is_eager=True,
    callback=apropos,
)
@click.option(
    "--list",
    "-l",
    help="Show this message, listing all available frecklets.",
    is_flag="true",
    is_eager=True,
    callback=help_all,
)
@click.option(
    "--help",
    "-h",
    help="Show this message",
    is_flag="true",
    is_eager=True,
    callback=help_only,
)
@click.pass_context
def cli(ctx, vars, **kwargs):
    """Execute frecklets using an auto-generated command-line interface.

    frecklecute supports executing any frecklet that is available in the current context as well as external ones. If the
    selected FRECKLET option is a file and exists, it will be parsed, validated, and executed. If not, a context-lookup
    will be performed and, if found, that frecklet will be used.

    In case no frecklet is found with the provided command, that command is interpreted as frecklet content in either
    'yaml', 'json', or 'toml' format and frecklecute will attempt to parse and run this.

    Use the '--list' option to get a list of all available frecklets in the current context, or '--apropos <search_term>'
    for a filtered list.
    """

    pass


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover

if getattr(sys, "frozen", False):
    cli(sys.argv[1:])
