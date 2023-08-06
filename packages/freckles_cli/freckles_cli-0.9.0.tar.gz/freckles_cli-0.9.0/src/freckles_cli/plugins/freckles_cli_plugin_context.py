# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import io
import os
import sys

import click
from click import Choice
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap

# from freckles.context import check_config_locked
from freckles.defaults import EXTERNAL_FOLDER as FRECKLES_EXTERNAL_FOLDER
from freckles.defaults import FRECKLES_CONFIG_DIR
from frutils import readable, unsorted_to_sorted_dict
from frutils.frutils_cli import output

yaml = YAML()


def fail_if_locked(context):

    locked = not context._config.config_unlocked
    if locked:
        click.echo(
            "\nThe initial freckles configuration is locked. Use the following command to unlock:\n\nfreckles context unlock\n\nFor more information, please visit: https://freckles.io/doc/configuration"
        )
        sys.exit(1)


@click.group()
@click.pass_context
def context(ctx):
    """Context-related tasks."""

    pass


@context.command("unlock")
@click.pass_context
def unlock_config(ctx):
    """Unlock configuration for advanced usage.

    By default, freckles does not allow the use of remote repositories (except for the 'community' one), as well as other
    security-relevant features. Those must be explicitly enabled after unlocking the configuration, which is done with this
    command.

    You can do this manually by creating an appropriate (YAML) configuration file under $HOME/.config/freckles/default.context that
    includes the key/value pair:

        accept_freckles_license: true

    For more information, please check out: https://freckles.io/doc/configuration

    """

    context = ctx.obj["context"]

    unlock_text_file = os.path.join(
        FRECKLES_EXTERNAL_FOLDER, "docs", "unlock_config_text.md"
    )

    with io.open(unlock_text_file, "r", encoding="utf-8") as f:
        unlock_text = f.read()

    # rendered = mdv.main(unlock_text, no_colors=True, header_nrs="1-")
    click.echo()
    click.echo(unlock_text)

    click.echo()

    input = click.prompt(
        "Unlock config, accept license",
        default="no",
        type=Choice(choices=["yes", "no"], case_sensitive=False),
    )

    if input.lower() == "no":
        click.echo("\nNo changes made.")
        sys.exit(0)

    input = click.prompt(
        "Use 'community' repo by default",
        default="no",
        type=Choice(choices=["yes", "no"], case_sensitive=False),
    )
    if input.lower() == "no":
        community = False
    else:
        community = True

    context.unlock_config(user_accepts=True, use_community=community)


@context.command("show", short_help="print current configuration")
@click.option("--show-interpreters", "-i", help="show interpreted data", is_flag=True)
@click.option(
    "--limit-interpreters",
    "-l",
    help="only display interpreter data for interpreters that contain this string (implies '--show-interpreters')",
)
@click.pass_context
def show_current(ctx, show_interpreters, limit_interpreters):
    """Print the current configuration, including documentation (optional).

    This will print the global configuration key/value pairs, as well as the interpreted ones for each added
    configuration interperter.
    """
    output_format = "yaml"

    context = ctx.obj["context"]
    run_config = ctx.obj["run_config"]

    cnf = context._config.cnf

    config_values = cnf.config
    indent = 0
    if limit_interpreters:
        show_interpreters = True
    if show_interpreters:
        indent = 2
    config_values_string = readable(
        unsorted_to_sorted_dict(config_values), out=output_format, indent=indent
    )

    click.echo()
    if show_interpreters:
        click.secho("Configuration", bold=True)
        click.secho("-------------", bold=True)
        click.echo()

    click.echo(config_values_string)
    click.echo()

    if not show_interpreters:
        sys.exit()

    click.secho("Interpreters", bold=True)
    click.secho("------------", bold=True)
    click.echo()

    for c_name in cnf.get_interpreter_names():

        interpreter = cnf.get_interpreter(c_name)

        if limit_interpreters and limit_interpreters not in c_name:
            continue

        title = c_name
        click.secho("  {}".format(title), bold=True)
        click.echo()

        validated = interpreter.overlay(run_config)

        if not validated:
            click.echo("    No configuration.")
            click.echo()
            continue

        details = CommentedMap()

        for k, schema in sorted(interpreter.schema.items()):
            v = validated.get(k, None)
            full = interpreter.get_doc_for_key(k)
            short_help = full.get_short_help()
            details[k] = CommentedMap()
            details[k]["desc"] = short_help
            if v is None:
                v = "n/a"
            details[k]["current value"] = v
            details[k]["default"] = schema.get("default", "n/a")

        for k, v in details.items():
            if details:
                click.secho("    {}:".format(k), bold=True)
                temp = readable(v, out=output_format, indent=6)
                click.echo(temp.rstrip())

        click.echo()

    # click.echo()


@context.command("doc", short_help="display documentation for config keys")
@click.option(
    "--limit-interpreters",
    "-l",
    help="only display interpreter data for interpreters that contain this string",
)
# @click.argument("key", required=False, nargs=-1)
@click.pass_context
def config_doc(ctx, limit_interpreters):
    """
    Displays documentation for configuration keys.
    """

    # output_format = "yaml"
    context = ctx.obj["context"]

    click.echo()

    for c_name in context.cnf.get_interpreter_names():
        if limit_interpreters and limit_interpreters not in c_name:
            continue

        interpreter = context.cnf.get_interpreter(c_name)
        # interpreter_type = interpreter_details["type"]

        click.secho("{}".format(c_name), bold=True)
        click.echo()
        schema = interpreter.schema

        key = False
        if not key:

            if not schema:
                click.echo("  No config schema")
                click.echo()
                continue

            for c_key in sorted(interpreter.schema.keys()):
                doc = interpreter.get_doc_for_key(c_key)
                click.secho(" {} ".format(c_key), bold=True, nl=False)
                key_schema = interpreter.get_schema_for_key(c_key)
                value_type = key_schema.get("type", "unknown_type")
                click.echo("({})".format(value_type))
                click.echo("    {}".format(doc.get_short_help()))
        # else:
        #     for doc_key in key:
        #         doc = interpreter.get_doc_for_key(doc_key)
        #         click.secho(" {} ".format(doc_key), bold=True, nl=False)
        #         if not schema or doc is None:
        #             click.echo("not used")
        #         else:
        #
        #             if doc_key in interpreter._target_attr_map.values():
        #                 # temp = []
        #                 # for k, v in interpreter.keymap.items():
        #                 #     if v == key:
        #                 #         temp.append(k)
        #                 # click.echo("not used, but alias for: {}".format(", ".join(temp)))
        #                 click.echo("not used")
        #                 continue
        #
        #             key_schema = interpreter.get_schema_for_key(doc_key)
        #             value_type = key_schema.get("type", "unknown_type")
        #             click.echo("({})".format(value_type))
        #             click.echo()
        #             click.secho("    desc: ", bold=True, nl=False)
        #             click.echo("{}".format(doc.get_short_help()))
        #             click.secho("    default: ", bold=True, nl=False)
        #             default = key_schema.get("default", "n/a")
        #             click.echo(default)
        #             current = cnf.config.get(c_name, doc_key, default="n/a")
        #             click.secho("    current: ", bold=True, nl=False)
        #             click.echo(current)
        #         click.echo()

        click.echo()


@context.command("copy", short_help="copy current configuration to new context")
@click.argument("context_name", nargs=1)
@click.option(
    "--edit",
    "-e",
    is_flag=True,
    default=False,
    help="open new context configuration in editor after copying",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    default=False,
    help="overwrite context configuration if already exists",
)
@click.pass_context
def copy(ctx, context_name, edit, force):
    """Copies the current configuration into a new context configuration file.

    The context configuration files are YAML text files which are stored under $HOME/.config/freckles with a '.context'
    filename extension.
    """

    context = ctx.obj["context"]
    fail_if_locked(context)
    cnf = ctx.obj["context"].config.cnf

    target = os.path.join(FRECKLES_CONFIG_DIR, "{}.context".format(context_name))
    try:
        cnf.save_current(target, force=force)
    except (Exception) as e:
        click.echo(e)
        sys.exit()

    if edit:
        click.edit(filename=target)


@context.command("delete", short_help="delete configuration profile")
@click.argument("profile_name", metavar="PROFILE_NAME", nargs=1)
@click.pass_context
def delete_profile(ctx, profile_name):
    """Deletes a context configuration.

    The configuration file is located under $HOME/.config/freckles (or $HOME/.freckles)
    """

    context = ctx.obj["context"]
    fail_if_locked(context)

    file = os.path.join(FRECKLES_CONFIG_DIR, "{}.context".format(profile_name))

    if os.path.exists(file):
        os.remove(file)


@context.command("edit", short_help="edit a context configuration")
@click.argument("profile_name", metavar="PROFILE_NAME", nargs=1, default="default")
@click.pass_context
def edit_profile(ctx, profile_name):
    """Edits a context configuration with the default editor.

    """

    context = ctx.obj["context"]
    fail_if_locked(context)

    path = os.path.join(FRECKLES_CONFIG_DIR, "{}.context".format(profile_name))
    click.edit(filename=path)


@context.command("list", short_help="list all available contexts")
@click.option(
    "--details", "-d", help="show contents of each context profile", is_flag=True
)
@click.pass_context
def list_contexts(ctx, details):
    """Lists all available context configurations."""

    freckles = ctx.obj["freckles"]

    click.echo()
    for context_name, context in freckles._context_configs.items():
        if not details:
            print(context_name)
            continue

        click.secho(context_name, bold=True)
        click.echo()
        output(context.config_dict, output_type="yaml", sort_keys=True)
        click.echo()


@context.command("add", short_help="add a context configuration from a template")
@click.option(
    "--edit",
    "-e",
    is_flag=True,
    default=False,
    help="open new context configuration in editor after copying",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    default=False,
    help="overwrite context configuration if already exists",
)
@click.option("--name", "-n", help="name of the context, defaults to template name")
@click.argument("template", type=str, nargs=1)
@click.pass_context
def add_context(ctx, template, edit, force, name):

    context = ctx.obj["context"]
    fail_if_locked(context)

    templates = {
        "latest": {
            "repos": [
                "frecklets::gl:frecklets/frecklets-nsbl-default",
                "roles::gl:frecklets/frecklets-nsbl-default-resources",
                "tasklists::gl:frecklets/frecklets-nsbl-default-resources",
                "temptings::gl:frecklets/temptings-default",
                "user",
            ]
        }
    }

    if template not in templates.keys():
        click.echo()
        click.echo("Template '{}' not available.".format(template))
        sys.exit(1)

    if not name:
        name = template

    target = os.path.join(FRECKLES_CONFIG_DIR, "{}.context".format(name))

    if os.path.exists(target):
        if not force:
            click.echo()
            click.echo(
                "Context config file '{}' already exists. Use the '--force' flag to overwrite.".format(
                    target
                )
            )
            sys.exit(1)
        else:
            os.remove(target)

    t = copy.copy(templates[template])
    if target == "default":
        t["accept_freckles_license"] = True

    try:
        with io.open(target, "w", encoding="utf-8") as f:
            yaml.dump(templates[template], f)
    except (Exception) as e:
        click.echo(e)
        sys.exit()

    if edit:
        click.edit(filename=target)
