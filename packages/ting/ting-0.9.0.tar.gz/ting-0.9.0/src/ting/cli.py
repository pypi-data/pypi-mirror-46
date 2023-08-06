# -*- coding: utf-8 -*-

"""Console script for tempting."""
import logging
import sys

import click
import click_log
from click import MultiCommand

from . import print_version


class TingMultiCommand(MultiCommand):
    def __init__(
        self,
        print_version_callback=print_version,
        name=None,
        invoke_without_command=False,
        no_args_is_help=None,
        subcommand_metavar=None,
        chain=False,
        result_callback=None,
        **kwargs
    ):

        super(TingMultiCommand, self).__init__(
            name=name,
            invoke_without_command=invoke_without_command,
            no_args_is_help=no_args_is_help,
            subcommand_metavar=subcommand_metavar,
            chain=chain,
            result_callback=result_callback,
            **kwargs
        )
        self.print_version_callback = print_version_callback
        self.path = None
        self.show_vars = False
        self.index = None
        self.index_cache = {}

    def list_commands(self, ctx):

        return []

    def get_command(self, ctx, cmd_name):

        print(cmd_name)
        return None


@click.command(name="ting", cls=TingMultiCommand, subcommand_metavar="Ting")
@click_log.simple_verbosity_option(logging.getLogger(), "--verbosity")
@click.pass_context
def cli(ctx, **kwargs):
    """Ting command line interface.
    """

    pass


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
