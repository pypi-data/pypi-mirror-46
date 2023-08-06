
from abc import ABC, abstractmethod

from Settings.RepoSettings import RepoSettings


class DiprCommandBase(ABC):

    def __init__(self, user_settings):
        self.user_settings = user_settings

    def _open_repo(self, arguments):
        r = RepoSettings(arguments.common.root_repo_path, self.user_settings)

        r.load_repo_files()
        r.resolve_repos()

        return r

    @abstractmethod
    def execute(self, arguments):
        pass
