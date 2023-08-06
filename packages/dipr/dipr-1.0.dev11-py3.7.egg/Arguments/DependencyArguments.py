from Arguments.ReposArguments import RepoArguments


class DependencyArguments(RepoArguments):
    DEPENDENCY_COMMAND = "depends"

    def __init__(self, root_parser, root_subparsers):
        super().__init__(root_parser, root_subparsers, DependencyArguments.DEPENDENCY_COMMAND,
                         "Maintain, add, or remove dependencies.")
