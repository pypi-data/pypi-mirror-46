import argparse

from Arguments.CommonArguments import CommonArguments
from Arguments.InitArguments import InitArguments
from Arguments.ImportArguments import ImportArguments
from Arguments.StatusArguments import StatusArguments
from Arguments.PullArguments import PullArguments
from Arguments.DependencyArguments import DependencyArguments
from Arguments.SubReposArguments import SubReposArguments
from Arguments.SourcesArguments import SourcesArguments
from Arguments.UpdateArguments import UpdateArguments
from Arguments.RcsArguments import RcsArguments
from Arguments.VersionArguments import VersionArguments


class DiprArguments(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="dipr")
        self.subparsers = self.parser.add_subparsers(help="Available dipr commands.", dest='g_command',
                                                     metavar="<command>")
        self.subparsers.required = True
        self.args = None
        self.remaining_args = None

        self.common = CommonArguments(self.parser, self.subparsers)
        self.init_command = InitArguments(self.parser, self.subparsers)
        self.import_command = ImportArguments(self.parser, self.subparsers)
        self.status_command = StatusArguments(self.parser, self.subparsers)
        self.sources_command = SourcesArguments(self.parser, self.subparsers)
        self.depends_command = DependencyArguments(self.parser, self.subparsers)
        self.subrepos_command = SubReposArguments(self.parser, self.subparsers)
        self.pull_command = PullArguments(self.parser, self.subparsers)
        self.update_command = UpdateArguments(self.parser, self.subparsers)
        self.rcs_command = RcsArguments(self.parser, self.subparsers)
        self.version_command = VersionArguments(self.parser, self.subparsers)

    @property
    def command(self):
        return self.args.g_command

    def parse_arguments(self, command_line=None):
        if command_line:
            self.args = self.parser.parse_args(command_line)
        else:
            self.args = self.parser.parse_args()

        self.common.set_args(self.args)
        self.init_command.set_args(self.args)
        self.import_command.set_args(self.args)
        self.status_command.set_args(self.args)
        self.sources_command.set_args(self.args)
        self.depends_command.set_args(self.args)
        self.subrepos_command.set_args(self.args)
        self.pull_command.set_args(self.args)
        self.update_command.set_args(self.args)
        self.rcs_command.set_args(self.args)
        self.version_command.set_args(self.args)
