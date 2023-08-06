import os
import sys

from Utilities.Console import Console

from Settings.GlobalSettings import GlobalSettings
from Settings.UserSettings import UserSettings

from Arguments import *
from Commands import *

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), ".."))


def main(command_line=sys.argv[1:]):
    args = DiprArguments()

    args.parse_arguments(command_line)

    Console.configure_logging(args.common.verbose)

    global_settings = GlobalSettings(__location__)
    user_settings = UserSettings(global_settings)

    if not user_settings.is_initialized:
        user_settings.initialize()

    all_commands = {
        InitArguments.INIT_COMMAND : InitCommand(user_settings),
        ImportArguments.IMPORT_COMMAND: ImportCommand(user_settings),
        StatusArguments.STATUS_COMMAND: StatusCommand(user_settings),
        SourcesArguments.SOURCES_COMMAND: SourcesCommand(user_settings),
        DependencyArguments.DEPENDENCY_COMMAND: DependsCommand(user_settings),
        SubReposArguments.SUBREPOS_COMMAND: SubReposCommand(user_settings),
        PullArguments.PULL_COMMAND: PullCommand(user_settings),
        UpdateArguments.UPDATE_COMMAND: UpdateCommand(user_settings),
        RcsArguments.RCS_COMMAND: RcsCommand(user_settings),
        VersionArguments.VERSION_COMMAND: VersionCommand(user_settings)
    }

    command = str.lower(args.command)

    Console.debug("Command: {}".format(command))

    if command in all_commands:
        all_commands[command].execute(args)
    else:
        Console.error("Invalid command: " + command)