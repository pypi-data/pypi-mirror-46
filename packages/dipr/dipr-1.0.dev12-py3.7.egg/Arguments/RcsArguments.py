from Arguments.ArgumentBase import ArgumentBase


class RcsArguments(ArgumentBase):
    RCS_COMMAND = "rcs"

    def __init__(self, root_parser, root_subparsers):
        super().__init__(root_parser, root_subparsers)

        self.init_parser = self.__initialize_parameters()

    def __initialize_parameters(self):
        parser = self.root_subparsers.add_parser(RcsArguments.RCS_COMMAND,
                                                 help="Issue revision control commands to base and sub repos.")

        rcs_commands = parser.add_subparsers(help="Revision control commands for root and sub repos.",
                                             dest="rcs_command",
                                             metavar="<rcs command>")
        rcs_commands.required = True

        RcsArguments.__initialize_commit(rcs_commands)
        RcsArguments.__initialize_tag(rcs_commands)
        RcsArguments.__initialize_push(rcs_commands)
        RcsArguments.__initialize_discard(rcs_commands)

        return rcs_commands

    @staticmethod
    def __initialize_add_common(command, include_message=False):
        command.add_argument("--exclude-root", required=False, action="store_true", dest="rcs_exclude_root",
                             help="Exclude the root repo from the operation.")

        command.add_argument("--exclude-subs", required=False, action="store_true", dest="rcs_exclude_subs",
                             help="Exclude the sub repos from the operation.")

        if include_message:
            command.add_argument("--message", "-m", default="", dest="rcs_message", metavar="message",
                                 help="Specify a message for the tag/commit.")

    @staticmethod
    def __initialize_commit(rcs_commands):
        add_command = rcs_commands.add_parser("commit", help="Commit changes to base and/or sub repos.")

        RcsArguments.__initialize_add_common(add_command, True)

        add_command.add_argument("--add-remove", required=False, action="store_true", dest="rcs_add_remove",
                                 help="If specified any unadded files will be added and any missing will be removed "
                                      "automatically")

    @staticmethod
    def __initialize_tag(rcs_commands):
        tag_command = rcs_commands.add_parser("tag", help="Add a tag to base and/or sub repos.")

        tag_command.add_argument("rcs_tag_name", nargs=1, metavar="<tag>", help="The name to give the tag.")

        RcsArguments.__initialize_add_common(tag_command, True)

    @staticmethod
    def __initialize_push(rcs_commands):
        push_command = rcs_commands.add_parser("push", help="Push base and/or sub repos to their remotes.")

        RcsArguments.__initialize_add_common(push_command, False)

        push_command.add_argument("--force", required=False, action="store_true", dest="rcs_force",
                                  help="Force the push to the remote repo.")

    @staticmethod
    def __initialize_discard(rcs_commands):
        discard_command = rcs_commands.add_parser("discard", help="Discard all changes in one or more repos.")

        RcsArguments.__initialize_add_common(discard_command, False)

        discard_command.add_argument("--include-depends", required=False, action="store_true",
                                     dest="rcs_include_depends",
                                     help="Include the dependency repos when discarding changes.")

        discard_command.add_argument("--only-depends", required=False, action="store_true", dest="rcs_only_depends",
                                     help="Only use the dependency repos when discarding changes.")

    @property
    def command(self):
        return self.args.rcs_command

    @property
    def message(self):
        return self.args.rcs_message

    @property
    def exclude_root(self):
        return self.args.rcs_exclude_root or self.only_depends

    @property
    def exclude_subrepos(self):
        return self.args.rcs_exclude_subs or self.only_depends

    @property
    def add_remove(self):
        return self.args.rcs_add_remove

    @property
    def force(self):
        return self.args.rcs_force

    @property
    def tag_name(self):
        if not self.args.rcs_tag_name:
            return ""

        return "_".join(self.args.rcs_tag_name[0].split())

    @property
    def include_depends(self):
        return hasattr(self, 'rcs_include_depends') and self.args.rc_include_depends or self.only_depends

    @property
    def only_depends(self):
        return hasattr(self, 'rcs_only_depends') and self.args.rcs_only_depends
