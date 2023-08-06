from Arguments.ArgumentBase import ArgumentBase


class UpdateArguments(ArgumentBase):
    UPDATE_COMMAND = "update"

    def __init__(self, root_parser, root_subparsers):
        super().__init__(root_parser, root_subparsers)

        self.__initialize_parameters()

    def __initialize_parameters(self):
        parser = self.root_subparsers.add_parser(UpdateArguments.UPDATE_COMMAND,
                                                 help="Set dependencies and/or subrepos to the desired revision.")

        parser.add_argument("-d", "--depends", action='store_true', help="Only pull dependencies.",
                            dest="c_update_depends")

        parser.add_argument("-s", "--subrepos", action='store_true', help="Only pull subrepos.",
                            dest="c_update_subrepos")

        parser.add_argument("-r", "--reset", action='store_true',
                            help="Remove any un-committed changes before updating.",
                            dest="c_update_reset_repo")

    @property
    def depends_only(self):
        return self.args.c_update_depends

    @property
    def subrepos_only(self):
        return self.args.c_update_subrepos

    @property
    def reset(self):
        return self.args.c_update_reset_repo

    @property
    def all_repos(self):
        return not self.depends_only and not self.subrepos_only