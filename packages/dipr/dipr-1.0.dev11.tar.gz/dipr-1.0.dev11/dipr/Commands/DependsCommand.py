
from Utilities.Console import Console

from Commands.RepoCommandBase import RepoCommandBase


class DependsCommand(RepoCommandBase):

    def __init__(self, user_settings):
        super().__init__(user_settings)

    def _get_arguments(self, arguments):
        return arguments.depends_command

    def _open_repos(self, repo_settings, arguments):
        return repo_settings.dependencies

    def _open_resolved_repos(self, repo_settings, arguments):
        return repo_settings.resolved_dependencies

    def _save_repos(self, repos, repo_settings, arguments):
        repo_settings.save_dependencies()
