from Arguments.ReposArguments import RepoArguments


class SubReposArguments(RepoArguments):
    SUBREPOS_COMMAND = "subrepos"

    def __init__(self, root_parser, root_subparsers):
        super().__init__(root_parser, root_subparsers, SubReposArguments.SUBREPOS_COMMAND,
                         "Maintain, add, or remove sub-repos.")
