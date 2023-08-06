from Arguments.ArgumentBase import ArgumentBase


class PullArguments(ArgumentBase):
    PULL_COMMAND = "pull"

    def __init__(self, root_parser, root_subparsers):
        super().__init__(root_parser, root_subparsers)

        self.__initialize_parameters()

    def __initialize_parameters(self):
        parser = self.root_subparsers.add_parser(PullArguments.PULL_COMMAND,
                                                 help="Pull dependencies or subrepos to local repos.")

        parser.add_argument("-d", "--depends", action='store_true', help="Only pull dependencies.",
                            dest="c_pull_depends")

        parser.add_argument("-s", "--subrepos", action='store_true', help="Only pull subrepos.",
                            dest="c_pull_subrepos")

        parser.add_argument("-u", "--update", action='store_true',
                            help="Update to the appropriate version after pulling.", dest="c_pull_update")

    @property
    def depends_only(self):
        return self.args.c_pull_depends

    @property
    def subrepos_only(self):
        return self.args.c_pull_subrepos

    @property
    def all_repos(self):
        return not self.depends_only and not self.subrepos_only

    @property
    def update(self):
        return hasattr(self.args, 'c_pull_update') and self.args.c_pull_update
