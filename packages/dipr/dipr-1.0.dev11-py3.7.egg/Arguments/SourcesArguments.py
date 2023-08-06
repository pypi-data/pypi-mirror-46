
import argparse

from Arguments.ArgumentBase import *
from Protocols import ProtocolHelper


class SourcesArguments(ArgumentBase):

    SOURCES_COMMAND = "sources"

    def __init__(self, root_parser, root_subparsers):
        super().__init__(root_parser, root_subparsers)

        self.__initialize_parameters()

    def __initialize_parameters(self):
        parser = self.root_subparsers.add_parser(SourcesArguments.SOURCES_COMMAND, help="Maintain or list data sources.")

        src_commands = parser.add_subparsers(help="Source commands", dest="src_command",
                                             metavar="<source command>")
        src_commands.required = True

        SourcesArguments.__initialize_list_command(src_commands)

        SourcesArguments.__initialize_add_command(src_commands)

        SourcesArguments.__initialize_remove_command(src_commands)

        SourcesArguments.__initialize_cleanup_command(src_commands)

        return parser

    @staticmethod
    def __initialize_list_command(src_commands):
        src_commands.add_parser("list", help="List the available sources.")

    @staticmethod
    def __initialize_add_command(src_commands):
        add_command = src_commands.add_parser("add", help="Add a new source.")

        add_command.add_argument("src_add_protocol", nargs=1, metavar="<protocol>",
                                 help="One of the available supported protocols: " +
                                      ", ".join(ProtocolHelper.SUPPORTED_PROTOCOLS))

        add_command.add_argument("src_add_remove_key", nargs=1, metavar="<key>",
                                 help="The key that will be used to identify the source to depends/subrepos.")

        add_command.add_argument("src_add_url", nargs=1, metavar="<url>", help="The url to the source.")

        add_command.add_argument("src_remainders", nargs=argparse.REMAINDER, action=RemainderStore,
                                 metavar="[NAME=VALUE [NAME=VALUE ...]]",
                                 help="Zero or more name=value pairs that are added to the source configuration for "
                                      "optional properties.")

        add_command.add_argument("--replace", required=False, action="store_true", dest="src_add_replace",
                                 help="If true, and the key already exists, replace it with these settings.")

    @staticmethod
    def __initialize_remove_command(src_commands):
        remove_command = src_commands.add_parser("remove", help="Remove an existing source")

        remove_command.add_argument("src_add_remove_key", nargs=1, metavar="<key>",
                                    help="The key of the source to remove.")

        remove_command.add_argument("--preserve", action="store_true", dest="src_remove_preserve",
                                    help="If specified, any depends/subrepos relying on the key be preserved instead "
                                         "of being removed.")

        remove_command.add_argument("--clean", action="store_true", dest="src_remove_clean",
                                    help="If specified (and not --preserve), any depends/subrepos removed that already"
                                         "exit on disk will be deleted as well.  Use with caution.")

    @staticmethod
    def __initialize_cleanup_command(src_commands):
        cleanup_command = src_commands.add_parser("cleanup", help="Remove any unused sources from the source file.")

        cleanup_command.add_argument("--check", action="store_true", dest="src_cleanup_check",
                                     help="Check and display a list of sources that would be removed.")

    @property
    def command(self):
        return self.args.src_command

    @property
    def key(self):
        return self.args.src_add_remove_key[0]

    @property
    def protocol(self):
        return self.args.src_add_protocol[0]

    @property
    def url(self):
        return self.args.src_add_url[0]

    @property
    def replace(self):
        return self.args.src_add_replace

    @property
    def preserve(self):
        return self.args.src_remove_preserve

    @property
    def clean(self):
        return hasattr(self.args, 'src_remove_clean') and self.args.src_remove_clean

    @property
    def cleanup_check(self):
        return hasattr(self.args, 'src_cleanup_check') and self.args.src_cleanup_check
