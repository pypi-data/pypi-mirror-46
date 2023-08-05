"""
odoo-manager

Usage:
  odoo-manager hello
  odoo-manager setup [dependencies|mapping|version] [--no-update] [--yes] [--only=<modules>] [-v | --verbose]
  odoo-manager new (project|module) [--name=<project>] [-h | --help] [-v | --verbose]
  odoo-manager format
  odoo-manager -h | --help
  odoo-manager --version

Options:
  --no-update                       Only install new modules instead of updating
                                    existing.
  --yes                             Assume yes to all questions [default: False]
  --only=<modules>                  Only install a certain set of modules
                                    instead of everything in the manifest.
  -h --help                         Show this screen.
  --version                         Show version.
  --name=<project>                  Pass a name for the project.
  -v --verbose                      Enable verbose details.

Examples:
  odoo-manager hello
"""

import traceback
from inspect import getmembers, isclass
from docopt import docopt

import odoo_manager
from odoo_manager.core import shell, configs
from odoo_manager.cli.exceptions import CommandException


def main():
    import odoo_manager.cli.commands

    options = docopt(__doc__, version=odoo_manager.version)
    # configs.init()

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (option_name, option_passed) in options.items():
        if hasattr(odoo_manager.cli.commands, option_name) and option_passed:
            module = getattr(odoo_manager.cli.commands, option_name)
            commands = getmembers(module, isclass)
            command = [command[1] for command in commands if command[0] != "BaseCommand"][0]
            command = command(options)

            try:
                command.run()

            # We will never show verbose information directly about a
            # CommandException because the user should not need to see the
            # trace on these. These are meant for clear breaking points
            # that we catch and display to the user. These are not unexpected
            # errors.
            #
            # For example, if a project directory cannot be found, this
            # exception will be raised. The user only needs to know that
            # a project directory cannot be found, but not the full stack
            # trace for this error.
            except CommandException as e:
                shell.out("{}\n".format(str(e)), color=shell.COLOR_RED)

            # These are unexpected error, and we will display trace information
            # to the user to provide them more details about what is going on,
            # if they have the --verbose flag enabled.
            except Exception as e:
                if options.get("--verbose", False):
                    shell.out(traceback.format_exc(), color=shell.COLOR_RED)
                else:
                    shell.out("{}\n".format(e), color=shell.COLOR_RED)
