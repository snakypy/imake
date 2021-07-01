"""
iMake
~~~~~~~~

iMake is a command line tool to simplify commands in Python projects, discarding the
usability of a Makefile file


For more information, access: 'https://github.com/snakypy/imake'

:copyright: Copyright 2021-2021 by Snakypy team, see AUTHORS.
:license: MIT license, see LICENSE for details.
"""

import argparse
from argparse import RawTextHelpFormatter
from contextlib import suppress
from os import getcwd, system
from os.path import exists, join
from subprocess import DEVNULL, call
from sys import exit
from textwrap import dedent
from time import strftime
from typing import Union

from snakypy.helpers import FG, NONE, printer
from snakypy.helpers.decorators import denying_os
from snakypy.helpers.files import create_file, read_file
from tomlkit import parse
from tomlkit.exceptions import NonExistentKey, ParseError
from tomlkit.items import Array


class Base:
    INFO = {
        "name": "iMake",
        "org": "Snakypy Organization <https://github.com/snakypy>",
        "configuration_file": ".imake",
        "version": "0.2.0",
    }


class Main(Base):
    def __init__(self):
        Base.__init__(self)

    @staticmethod
    def load_conf() -> Union[dict, None]:
        try:
            file = read_file(join(getcwd(), Main().INFO["configuration_file"]))
            return dict(parse(file))
        except FileNotFoundError:
            printer(
                f'Configuration file does not exist. Create the "{Main().INFO["configuration_file"]}" file.',
                foreground=FG().ERROR,
            )
            exit(1)
        except ParseError:
            printer(
                "The configuration file is poorly defined. Fix it!",
                foreground=FG().ERROR,
            )
            exit(1)

    def create_base_config(self) -> None:
        if not exists(self.INFO["configuration_file"]):
            content = '[]\ndescription = ""\ninitial_message = ""\ncommands = []\nfinal_message = ""\n'
            create_file(content, self.INFO["configuration_file"])
            printer(
                f'File "{self.INFO["configuration_file"]}" created in this directory successfully.',
                foreground=FG().FINISH,
            )
        else:
            printer("Configuration file already exists.", foreground=FG().WARNING)

    def menu(self, config_toml: dict) -> argparse.Namespace:

        description_package = dedent(
            f"""
            {self.INFO["name"]} is a command line tool to simplify commands in Python projects, discarding the
            usability of a Makefile file.
        """
        )

        if len([args for args in config_toml]):
            usage = f"[init, version] [{', '.join([args for args in config_toml])} [--desc | --quiet]]"
            command_help = (
                f"{{{FG().BLUE}{', '.join([args for args in config_toml])}, init, version{NONE}}}\n"
                f"NOTE: For the description of each command use the --desc option."
            )
        else:
            usage = "[init, version]"
            command_help = f"{{{FG().BLUE}init, version{NONE}}}"

        parser = argparse.ArgumentParser(
            description=f"{FG().MAGENTA}{description_package}{NONE}",
            usage=f" {self.INFO['name'].lower()} [-h] {usage}",
            formatter_class=RawTextHelpFormatter,
            epilog=f"(c) {strftime('%Y')} - {self.INFO['org']}",
        )
        parser.add_argument(
            "command",
            nargs="?",
            metavar="command",
            help=f"Usage: {command_help}",
        )
        parser.add_argument(
            "-d",
            "--desc",
            action="store_true",
            default=False,
            help="show the description (if any) of each command",
        )
        parser.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            default=False,
            help="it does not show the output of the commands",
        )
        args = parser.parse_args()

        return args


@denying_os("nt")
def run():
    with suppress(TypeError):

        if exists(Main().INFO["configuration_file"]):
            menu = Main().menu(Main().load_conf())
        else:
            menu = Main().menu({})

        if menu.command == "version":
            printer(f"Version: {FG().CYAN}{Main().INFO['version']}{NONE}")
        elif menu.command == "init":
            Main().create_base_config()
        else:

            # Get configuration
            config_toml = Main().load_conf()

            # Show description command
            for args in config_toml:
                if menu.command not in config_toml:
                    printer(
                        f'Option "{menu.command}" invalid. I can\'t find the configuration file.',
                        foreground=FG().WARNING,
                    )
                    exit(1)
                if menu.command == args and menu.desc:
                    try:
                        printer(
                            f"{FG().BLUE}Description:{NONE}",
                            config_toml[args]["description"],
                            foreground=FG().MAGENTA,
                        )
                    except NonExistentKey:
                        printer(
                            "There is no description of this command.",
                            foreground=FG().WARNING,
                        )
                elif menu.command == args:

                    # Show header message
                    with suppress(NonExistentKey):
                        if not menu.quiet:
                            printer(
                                config_toml[args]["initial_message"],
                                foreground=FG().QUESTION,
                            )

                    # Starting commands
                    try:
                        if not type(config_toml[args]["commands"]) is Array:
                            printer(
                                'The "commands" key must be an array of commands. Aborted.',
                                foreground=FG().ERROR,
                            )
                            exit(1)
                        for r in config_toml[args]["commands"]:
                            if menu.quiet:
                                call(r, shell=True, stderr=DEVNULL, stdout=DEVNULL)
                            else:
                                system(r)
                    except NonExistentKey:
                        printer(
                            'The configuration file needs the "commands" key. Aborted.',
                            foreground=FG().ERROR,
                        )
                        exit(1)

                    # Show finish message
                    with suppress(NonExistentKey):
                        if not menu.quiet:
                            printer(
                                config_toml[args]["final_message"],
                                foreground=FG().FINISH,
                            )
