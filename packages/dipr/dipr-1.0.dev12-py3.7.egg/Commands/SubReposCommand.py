
from Utilities.Console import Console

from Commands.RepoCommandBase import RepoCommandBase


class SubReposCommand(RepoCommandBase):

    def __init__(self, user_settings):
        super().__init__(user_settings)

    def _get_arguments(self, arguments):
        return arguments.subrepos_command

    def _open_repos(self, repo_settings, arguments):
        return repo_settings.subrepos

    def _open_resolved_repos(self, repo_settings, arguments):
        return repo_settings.resolved_subrepos

    def _save_repos(self, repos, repo_settings, arguments):
        repo_settings.save_subrepos()
