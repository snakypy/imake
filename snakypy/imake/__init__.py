import argparse
from contextlib import suppress
from os import getcwd, system
from os.path import join
from sys import exit

from snakypy.helpers import FG, NONE, printer
from snakypy.helpers.files import read_file
from tomlkit import parse
from tomlkit.exceptions import NonExistentKey, ParseError
from tomlkit.items import Array


class Base:
    INFO = {
        "name": "Imake",
        "configuration_file": ".imake",
        "version": "0.1.0",
    }


class Imake(Base):
    def __init__(self):
        try:
            file = read_file(join(getcwd(), self.INFO["configuration_file"]))
            self.config_toml = dict(parse(file))
        except FileNotFoundError:
            printer(
                f'Configuration file does not exist. Create the "{self.INFO["configuration_file"]}" file',
                foreground=FG().ERROR,
            )
            exit(1)
        except ParseError:
            printer(
                "The configuration file is poorly defined. Fix it!",
                foreground=FG().ERROR,
            )
            exit(1)

    def menu(self):

        description_package = f"""
            {self.INFO["name"]} is a command line tool to simplify commands in Python projects, discarding the
            usability of a Makefile file.
        """

        if len([args for args in self.config_toml]):
            usage = f"[{', '.join([f'{args} [--desc]' for args in self.config_toml])}, version]"
            command_help = f"[{FG().BLUE}{', '.join([args for args in self.config_toml])}, version{NONE}]"
        else:
            usage = f"[version]"
            command_help = f"[{FG().BLUE}version{NONE}]"

        parser = argparse.ArgumentParser(
            description=f"{FG().MAGENTA}{description_package}{NONE}",
            usage=f" imake [-h] {usage}",
        )
        parser.add_argument(
            "command",
            nargs="?",
            help=command_help,
        )
        parser.add_argument(
            "--desc",
            action="store_true",
            default=False,
            help="show the description (if any) of each command.",
        )
        args = parser.parse_args()

        return args


def main():
    with suppress(TypeError):
        imake = Imake()

        if imake.menu().command == "version":
            printer(f"Version: {FG().CYAN}{imake.INFO['version']}{NONE}")
        else:
            for args in imake.config_toml:
                if imake.menu().command == args and imake.menu().desc:
                    try:
                        printer(
                            f"{FG().BLUE}Command description:{NONE}",
                            imake.config_toml[args]["description"],
                            foreground=FG().MAGENTA,
                        )
                    except NonExistentKey:
                        printer(
                            "There is no description of this command.",
                            foreground=FG().WARNING,
                        )
                elif imake.menu().command == args:
                    with suppress(NonExistentKey):
                        printer(
                            imake.config_toml[args]["header"], foreground=FG().QUESTION
                        )
                    try:
                        if not type(imake.config_toml[args]["commands"]) is Array:
                            printer(
                                'The "commands" key must be an array of commands. Aborted',
                                foreground=FG().ERROR,
                            )
                            exit(1)
                        for r in imake.config_toml[args]["commands"]:
                            system(r)
                    except NonExistentKey:
                        printer(
                            'The configuration file needs the "commands" key. Aborted.',
                            foreground=FG().ERROR,
                        )
                        exit(1)

                    with suppress(NonExistentKey):
                        printer(
                            imake.config_toml[args]["footer"], foreground=FG().FINISH
                        )
