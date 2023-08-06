# -*- coding: utf-8 -*-
import copy
import logging
import sys

import click
import click_log
import colorama
from stevedore.extension import ExtensionManager

from ..freckles_base_cli import FrecklesBaseCommand, run_frecklet, handle_exception

log = logging.getLogger("freckles")
click_log.basic_config(log)


colorama.init()

VARS_HELP = "variables to be used for templating, can be overridden by cli options if applicable"
DEFAULTS_HELP = "default variables, can be used instead (or in addition) to user input via command-line parameters"
KEEP_METADATA_HELP = "keep metadata in result directory, mostly useful for debugging"
FRECKLECUTE_EPILOG_TEXT = "freckles is free to use in combination with open source software, for information on private licenses visit: https://freckles.io"


# extensions
# ------------------------------------------------------------------------
def load_plugins():
    """Loading a dictlet finder extension.

    Returns:
      ExtensionManager: the extension manager holding the extensions
    """

    log2 = logging.getLogger("stevedore")
    out_hdlr = logging.StreamHandler(sys.stderr)
    out_hdlr.setFormatter(logging.Formatter("freckles plugin error -> %(message)s"))
    out_hdlr.setLevel(logging.DEBUG)
    log2.addHandler(out_hdlr)
    log2.setLevel(logging.INFO)

    log.debug("Loading freckles plugin...")

    mgr = ExtensionManager(
        namespace="freckles_cli.plugins",
        invoke_on_load=False,
        propagate_map_exceptions=True,
    )

    return mgr


class FrecklesCommand(FrecklesBaseCommand):
    def __init__(self, *args, **kwargs):

        super(FrecklesCommand, self).__init__(invoke_without_command=True, **kwargs)
        self.plugins = load_plugins()
        self.commands = {}
        for plugin in self.plugins:
            name = plugin.name
            ep = plugin.entry_point
            command = ep.load()
            self.commands[name] = command

    def list_freckles_commands(self, ctx):

        return sorted(self.commands.keys())

    def get_freckles_command(self, ctx, name, **kwargs):

        # ctx.obj["control_dict"] = self.control_dict
        ctx.obj["run_config"] = self.run_config

        command = self.commands.get(name, None)

        if command:
            return command

        try:
            frecklet, frecklet_name = self.context.load_frecklet(name, validate=True)

            @click.command(name=name)
            def command(*args, **kwargs):

                click.echo()

                vars = copy.deepcopy(self.extra_vars)

                try:
                    run_frecklet(
                        ctx=ctx,
                        frecklet=frecklet,
                        freckles_context=self.context,
                        run_config=self.run_config,
                        vars=vars,
                    )
                except (Exception) as e:
                    handle_exception(e)

            return command

        except (Exception) as e:
            handle_exception(e)


@click.command(
    name="freckles",
    cls=FrecklesCommand,
    epilog=FRECKLECUTE_EPILOG_TEXT,
    subcommand_metavar="PLUGIN",
)
# @click.option("--vars", "-v", help="additional vars", multiple=True, type=VarsType())
@click_log.simple_verbosity_option(logging.getLogger(), "--verbosity")
@click.pass_context
def cli(ctx, vars, **kwargs):
    """The 'freckles' command-line tool is the central application in the freckles package.

    It allows users to configure the application itself, manage contexts and adapters, list
    available frecklets and their details, and, most importantly, run and debug those frecklets.

    The freckles package provides other applications (most notably: frecklecute) that allow to do some of those tasks in easier ways, but in a pinch users could do without those, as long as the 'freckles' commmand-line app is available.

    """

    pass
    #
    # if ctx.invoked_subcommand is not None or sys.stdin.isatty():
    #     return
    #
    # frecklet_data = []
    #
    # stream = click.get_text_stream("stdin", encoding="utf-8")
    #
    # for line in stream:
    #     frecklet_data.append(line)
    #
    # frecklet_data = "".join(frecklet_data)
    #
    # command = ctx.command
    #
    # import pp
    # pp(command.__dict__)
    #
    # exe_func = command.get_command(ctx, frecklet_data)
    # exe_func()


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover

if getattr(sys, "frozen", False):
    cli(sys.argv[1:])
