from Arguments.ArgumentBase import ArgumentBase


class VersionArguments(ArgumentBase):
    VERSION_COMMAND = "version"

    def __init__(self, root_parser, root_subparsers):
        super().__init__(root_parser, root_subparsers)

        self.init_parser = self.__initialize_parameters()

    def __initialize_parameters(self):
        parser = self.root_subparsers.add_parser(VersionArguments.VERSION_COMMAND,
                                                 help="Display version information.")

        return parser
