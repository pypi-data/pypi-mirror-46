from Arguments.ArgumentBase import ArgumentBase


class StatusArguments(ArgumentBase):
    STATUS_COMMAND = "status"

    def __init__(self, root_parser, root_subparsers):
        super().__init__(root_parser, root_subparsers)

        self.init_parser = self.__initialize_parameters()

    def __initialize_parameters(self):
        parser = self.root_subparsers.add_parser(StatusArguments.STATUS_COMMAND,
                                                 help="Display the status of configured repos.")

        parser.add_argument("--all", action='store_true',
                            help="Display the status of all repos (default).", dest="status_all")

        parser.add_argument("--depends", action='store_true',
                            help="Display the status of dependencies.", dest="status_depends")

        parser.add_argument("--subrepos", action='store_true',
                            help="Display the status of subrepos.", dest="status_subrepos")

        return parser

    @property
    def all(self):
        return self.args.status_all or not (self.depends_only or self.subrepos_only)

    @property
    def depends_only(self):
        return self.args.status_depends

    @property
    def subrepos_only(self):
        return self.args.status_subrepos
