
from pathlib import Path

from Arguments.ArgumentBase import ArgumentBase


class CommonArguments(ArgumentBase):

    def __init__(self, root_parser, root_subparsers):
        super().__init__(root_parser, root_subparsers)

        self.__initialize_parameters()

    def __initialize_parameters(self):
        self.root_parser.add_argument("-p", "--path",
                                      help="Path to the working directory containing the .dip directory.",
                                      default=Path.cwd(), dest="c_root_repo_path", metavar="<repo path>")

        self.root_parser.add_argument("-v", "--verbose", help="Enable additional logging.", action="store_true",
                                      dest="c_verbose")
        
    @property
    def root_repo_path(self):
        return Path(self.args.c_root_repo_path)

    @property
    def verbose(self):
        return self.args.c_verbose

