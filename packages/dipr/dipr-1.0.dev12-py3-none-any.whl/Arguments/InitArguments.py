from Arguments.ArgumentBase import ArgumentBase


class InitArguments(ArgumentBase):
    INIT_COMMAND = "init"

    def __init__(self, root_parser, root_subparsers):
        super().__init__(root_parser, root_subparsers)

        self.init_parser = self.__initialize_parameters()

    def __initialize_parameters(self):
        parser = self.root_subparsers.add_parser(InitArguments.INIT_COMMAND,
                                                 help="Initialize a repo with the required dip files.")

        parser.add_argument("--force", action='store_true',
                            help="Force (re)initialization of the target repo.", dest="init_force")

        parser.add_argument("--noadd", action='store_true',
                            help="Do not add the new files to the repo.", dest="init_no_add")

        return parser

    @property
    def force(self):
        return self.args.init_force

    @property
    def no_add(self):
        return self.args.init_no_add
