from pathlib import PurePath

from Arguments.ArgumentBase import ArgumentBase


class RepoArguments(ArgumentBase):

    def __init__(self, root_parser, root_subparsers, command_name, help_text):
        super().__init__(root_parser, root_subparsers)

        self.parser = self.__initialize_parameters(command_name, help_text)

    def __initialize_parameters(self, command_name, help_text):
        parser = self.root_subparsers.add_parser(command_name, help=help_text)

        repo_commands = parser.add_subparsers(help="Repo commands", dest="repo_command",
                                              metavar="<repo command>")
        repo_commands.required = True

        RepoArguments.__initialize_list(repo_commands)
        RepoArguments.__initialize_add(repo_commands)
        RepoArguments.__initialize_remove(repo_commands)
        RepoArguments.__initialize_freeze(repo_commands)
        RepoArguments.__initialize_unfreeze(repo_commands)
        RepoArguments.__initialize_upgrade(repo_commands)
        RepoArguments.__initialize_rev(repo_commands)

        return repo_commands

    @staticmethod
    def __initialize_list(repo_commands):
        repo_commands.add_parser("list", help="List the available repos.")
        pass

    @staticmethod
    def __initialize_add(repo_commands):
        add_command = repo_commands.add_parser("add", help="Add a repo using a source key and path.")

        add_command.add_argument("repo_src_key_param", nargs=1, metavar="<key>",
                                 help="The source key for the repo.")

        add_command.add_argument("repo_local_path_param", nargs=1, metavar="<path>",
                                 help="The local relative path for the repo.")

        add_command.add_argument("--revision", dest="repo_set_revision", metavar="revision",
                                 help="Specify a hash as the revision for the repo.")

        add_command.add_argument("--tag", dest="repo_set_tag", metavar="tag",
                                 help="Specify a tag as the repo revision.")

        add_command.add_argument("--branch", dest="repo_set_branch", metavar="branch",
                                 help="Specify a branch to checkout for the repo revision.")

        add_command.add_argument("--replace", required=False, action="store_true", dest="repo_add_replace",
                                 help="Replace the repo if it already exists.")

    @staticmethod
    def __initialize_remove(repo_commands):
        remove_command = repo_commands.add_parser("remove", help="Remove a repo by its relative path.")

        remove_command.add_argument("--path", dest="repo_local_path_flag", metavar="<path>",
                                    help="Remove this specific repo from dip.")

        remove_command.add_argument("--key", dest="repo_src_key_flag", metavar="<key>",
                                    help="If specified, remove all repos that use this source key.")

        remove_command.add_argument("--clean", required=False, action="store_true", dest="repo_remove_clean",
                                    help="Remove the on disk contents as well.")

        pass

    @staticmethod
    def __initialize_freeze(repo_commands):
        freeze_command = repo_commands.add_parser("freeze", help="Freeze one or all repos at their current revision.")

        freeze_command.add_argument("--path", dest="repo_local_path_flag", metavar="<path>",
                                    help="Freeze this specific repo at its current revision.")

        freeze_command.add_argument("--key", dest="repo_src_key_flag", metavar="<key>",
                                    help="Freeze all repos using  this key at their current revision.")

    @staticmethod
    def __initialize_unfreeze(repo_commands):
        freeze_command = repo_commands.add_parser("unfreeze", help="Unfreeze one or all repos and set them to tip.")

        freeze_command.add_argument("--path", dest="repo_local_path_flag", metavar="<path>",
                                    help="Freeze this specific repo at its current revision.")

        freeze_command.add_argument("--key", dest="repo_src_key_flag", metavar="<key>",
                                    help="Freeze all repos using  this key at their current revision.")

    @staticmethod
    def __initialize_upgrade(repo_commands):
        upgrade_command = repo_commands.add_parser("upgrade",
                                                   help="Upgrade one or all repos to their latest tagged revision.")

        upgrade_command.add_argument("--path", dest="repo_local_path_flag", metavar="<path>",
                                     help="Upgrade this specific repo at its latest tagged revision.")

        upgrade_command.add_argument("--key", dest="repo_src_key_flag", metavar="<key>",
                                     help="Upgrade all repos using  this key at their latest tagged revision.")

        upgrade_command.add_argument("--check", required=False, action="store_true", dest="repo_upgrade_check",
                                     help="Check to see which repos can be upgraded.")

        upgrade_command.add_argument("--all", required=False, action="store_true", dest="repo_upgrade_all",
                                     help="Upgrade repos even if they are not currently set to a tag.")

        upgrade_command.add_argument("--update", required=False, action="store_true", dest="repo_upgrade_update",
                                     help="After upgrading the tag, do an update to set it to the new version.")

    @staticmethod
    def __initialize_rev(repo_commands):
        rev_command = repo_commands.add_parser("rev", help="Set one or all repos to a revision or to tip.")

        rev_command.add_argument("--path", dest="repo_local_path_flag", metavar="<path>",
                                 help="Discard changes for this specific repo.")

        rev_command.add_argument("--key", dest="repo_src_key_flag", metavar="<key>",
                                 help="Discard changes all repos using this key.")

        rev_command.add_argument("--tip", required=False, action="store_true", dest="repo_set_tip",
                                 help="If set, the specified repos will be set to their latest revision in their current branch.")

        rev_command.add_argument("--revision", dest="repo_set_revision", metavar="revision",
                                 help="Specify a hash as the revision for the repo.")

        rev_command.add_argument("--tag", dest="repo_set_tag", metavar="tag",
                                 help="Specify a tag as the repo revision.")

        rev_command.add_argument("--branch", dest="repo_set_branch", metavar="branch",
                                 help="Specify a branch to checkout for the repo revision.")

    @property
    def command(self):
        return self.args.repo_command

    @property
    def source_key(self):
        if hasattr(self.args, 'repo_src_key_param') and self.args.repo_src_key_param:
            return self.args.repo_src_key_param[0]
        elif hasattr(self.args, 'repo_src_key_flag') and self.args.repo_src_key_flag:
            return self.args.repo_src_key_flag
        else:
            return None

    @property
    def repo_local_path(self):
        if hasattr(self.args, 'repo_local_path_param') and self.args.repo_local_path_param:
            return PurePath(self.args.repo_local_path_param[0]).as_posix()
        elif hasattr(self.args, 'repo_local_path_flag') and self.args.repo_local_path_flag:
            return PurePath(self.args.repo_local_path_flag).as_posix()
        else:
            return None

    @property
    def revision(self):
        return self.args.repo_set_revision

    @property
    def tag(self):
        return self.args.repo_set_tag

    @property
    def branch(self):
        return self.args.repo_set_branch

    @property
    def clean(self):
        return self.args.repo_remove_clean

    @property
    def tip(self):
        return self.args.repo_set_tip

    @property
    def replace(self):
        return self.args.repo_add_replace

    @property
    def check(self):
        return self.args.repo_upgrade_check

    @property
    def upgrade_all(self):
        return self.args.repo_upgrade_all

    @property
    def update(self):
        return hasattr(self.args, 'repo_upgrade_update') and self.args.repo_upgrade_update
