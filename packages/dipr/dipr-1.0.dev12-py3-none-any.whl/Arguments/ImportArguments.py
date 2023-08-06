from Arguments.ArgumentBase import ArgumentBase


class ImportArguments(ArgumentBase):
    IMPORT_COMMAND = "import"

    GUESTREPO_SOURCE = "guestrepos"
    SUBMODULES_SOURCE = "submodules"
    GITLAB_SOURCE = "gitlab"

    IMPORT_SOURCES = [GUESTREPO_SOURCE, SUBMODULES_SOURCE, GITLAB_SOURCE]

    def __init__(self, root_parser, root_subparsers):
        super().__init__(root_parser, root_subparsers)

        self.init_parser = self.__initialize_parameters()

    def __initialize_parameters(self):
        parser = self.root_subparsers.add_parser(ImportArguments.IMPORT_COMMAND,
                                                 help="Import existing sources and repos from the base repo.")

        import_commands = parser.add_subparsers(help="Import commands", dest="import_command",
                                                metavar="<import command>")
        import_commands.required = True

        ImportArguments.__initialize_guestrepos_command(import_commands)

        ImportArguments.__initialize_submodules_command(import_commands)

        ImportArguments.__initialize_gitlab_command(import_commands)

        # parser.add_argument("import_source", metavar='source', type=str, nargs=1,
        #                     help="Import data source.  Available sources: " + ", ".join(ImportArguments.IMPORT_SOURCES))
        #
        # parser.add_argument("--clean", action='store_true', dest="import_clean",
        #                     help="Remove source files from the repo.  All files will be discarded.")
        #
        # parser.add_argument("--clean-force", action='store_true', dest="import_clean_yes",
        #                     help="Clean but don't prompt to warn of file removal.")
        #
        # parser.add_argument("--import-force", action='store_true', dest="import_force",
        #                     help="Force importing of sources and repos replacing any values that already have "
        #                          "existing keys.")

        return parser

    @staticmethod
    def __initialize_add_common(import_command, clean=True, clean_force=True, force=True):
        if clean:
            import_command.add_argument("--clean", action='store_true', dest="import_clean",
                                        help="Remove source files from the repo.  All files will be discarded.")

        if clean_force:
            import_command.add_argument("--clean-force", action='store_true', dest="import_clean_yes",
                                        help="Clean but don't prompt to warn of file removal.")

        if force:
            import_command.add_argument("--import-force", action='store_true', dest="import_force",
                                        help="Force importing of sources and repos replacing any values that already have "
                                             "existing keys.")

    @staticmethod
    def __initialize_guestrepos_command(import_commands):
        guestrepos_command = import_commands.add_parser(ImportArguments.GUESTREPO_SOURCE,
                                                        help="Import from guestrepos files.")

        ImportArguments.__initialize_add_common(guestrepos_command)

    @staticmethod
    def __initialize_submodules_command(import_commands):
        submodules_command = import_commands.add_parser(ImportArguments.SUBMODULES_SOURCE,
                                                        help="Import from git submodules.")

        ImportArguments.__initialize_add_common(submodules_command)

    @staticmethod
    def __initialize_gitlab_command(import_commands):
        gitlab_command = import_commands.add_parser(ImportArguments.GITLAB_SOURCE,
                                                    help="Import sources and repos from gitlab.")

        gitlab_command.add_argument("--token", "-t", default="", dest="gitlab_token", metavar="<token>",
                                    help="The authentication token to use with Gitlab.")

        gitlab_command.add_argument("--url", default="https://gitlab.com", dest="gitlab_url", metavar="<url>",
                                    help="The url used to access Gitlab (Default is https://gitlab.com).")

        gitlab_command.add_argument("--search", "-s", default=None, dest="gitlab_search", metavar="<search>",
                                    help="A string to match when returning Gitlab project results.")

        gitlab_command.add_argument("--sources-only", action='store_true', dest='gitlab_sources_only',
                                    help="Only import Gitlab projects as sources.")

        gitlab_command.add_argument("--include-membership", action='store_true', dest='gitlab_include_membership',
                                    help="Include Gitlab projects where the user is a member (default is owner only).")

        gitlab_command.add_argument("--as-depends", action="store_true", dest="gitlab_as_depends",
                                    help="Imported repos will be added as dependencies.")

        gitlab_command.add_argument("--as-subrepos", action="store_true", dest="gitlab_as_subrepos",
                                    help="Imported repos will be added as subrepos.")

        gitlab_command.add_argument("--depends-prefix", default="Depends", dest="gitlab_depends_prefix",
                                    metavar="<depends prefix>",
                                    help="The path prefix applied to dependencies (Default is Depends/).")

        gitlab_command.add_argument("--subrepos-prefix", default="Subrepos", dest="gitlab_subrepos_prefix",
                                    metavar="<subrepos prefix>",
                                    help="The path prefix applied to subrepos (Default is Subrepos/).")

        ImportArguments.__initialize_add_common(gitlab_command, clean=False, clean_force=False)

    @property
    def source(self):
        return self.args.import_command

    @property
    def clean(self):
        return self.args.import_clean or self.args.import_clean_yes

    @property
    def clean_yes(self):
        return self.args.import_clean_yes

    @property
    def force(self):
        return self.args.import_force

    @property
    def gitlab_sources_only(self):
        return hasattr(self.args, 'gitlab_sources_only') and self.args.gitlab_sources_only

    @property
    def gitlab_include_membership(self):
        return hasattr(self.args, 'gitlab_include_membership') and self.args.gitlab_include_membership

    @property
    def gitlab_token(self):
        if hasattr(self.args, 'gitlab_token'):
            return self.args.gitlab_token
        else:
            return None

    @property
    def gitlab_url(self):
        if hasattr(self.args, 'gitlab_url'):
            return self.args.gitlab_url
        else:
            return None

    @property
    def gitlab_search(self):
        if hasattr(self.args, "gitlab_search"):
            return self.args.gitlab_search
        else:
            return None

    @property
    def gitlab_as_depends(self):
        return (hasattr(self.args, 'gitlab_as_depends') and self.args.gitlab_as_depends) or not self.gitlab_as_subrepos

    @property
    def gitlab_as_subrepos(self):
        return hasattr(self.args, 'gitlab_as_subrepos') and self.args.gitlab_as_subrepos

    @property
    def gitlab_depends_prefix(self):
        if hasattr(self.args, "gitlab_depends_prefix"):
            return self.args.gitlab_depends_prefix
        else:
            return None

    @property
    def gitlab_subrepos_prefix(self):
        if hasattr(self.args, "gitlab_subrepos_prefix"):
            return self.args.gitlab_subrepos_prefix
        else:
            return None


