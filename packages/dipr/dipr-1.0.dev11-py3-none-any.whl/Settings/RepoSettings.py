
from shutil import copyfile
from datetime import datetime
import getpass
from pathlib import Path

from Utilities.Console import Console

from Repos.DiprSources import DiprSources
from Repos.DiprDependencies import DiprDependencies
from Repos.DiprSubRepos import DiprSubRepos
from Repos.DiprResolvedRepo import DiprResolvedRepo
from Protocols.ProtocolHelper import resolve_repo_handler


class RepoSettings(object):

    DIPR_REPO_DIR = '.dipr'

    DIPR_SRC_FILE = 'diprsrc.yaml'
    DIPR_DEP_FILE = 'diprdep.yaml'
    DIPR_SUB_FILE = 'diprsub.yaml'

    def __init__(self, repo_path, user_settings):
        self.root_repo_path = Path(repo_path)
        self.user_settings = user_settings

        self.dipr_repo_path = Path(self.root_repo_path, RepoSettings.DIPR_REPO_DIR)
        self.dipr_src_file_path = Path(self.dipr_repo_path, RepoSettings.DIPR_SRC_FILE)
        self.dipr_dep_file_path = Path(self.dipr_repo_path, RepoSettings.DIPR_DEP_FILE)
        self.dipr_sub_file_path = Path(self.dipr_repo_path, RepoSettings.DIPR_SUB_FILE)

        self.sources = DiprSources(self.dipr_src_file_path)
        self.dependencies = DiprDependencies(self.dipr_dep_file_path)
        self.subrepos = DiprSubRepos(self.dipr_sub_file_path)

        self.root_repo_handler = None
        self.resolved_dependencies = None
        self.resolved_subrepos = None

        self.resolved = False

    @property
    def is_initialized(self):
        return self.dipr_repo_path.is_dir() and\
               self.dipr_src_file_path.is_file() and\
               self.dipr_dep_file_path.is_file() and\
               self.dipr_sub_file_path.is_file()

    @staticmethod
    def __append_creation_information(file_path):
        with open(file_path, 'a') as file:
            file.write("# Created by " + getpass.getuser() + " at " + datetime.now().strftime("%I:%M%p on %B %d, %Y"))

    @staticmethod
    def __init_repo_file(source_path, destination_path, force):
        if force and destination_path.is_file():
            destination_path.unlink()

        if not destination_path.is_file():
            if source_path.is_file():
                copyfile(source_path, destination_path)

        RepoSettings.__append_creation_information(destination_path)

    def load_repo_files(self):
        self.sources.load()
        self.dependencies.load()
        self.subrepos.load()

    def initialize(self, force=False):
        if not force and self.is_initialized:
            return

        if not self.dipr_repo_path.is_dir():
            self.dipr_repo_path.mkdir()

        RepoSettings.__init_repo_file(self.user_settings.dipr_src_template_file_path, self.dipr_src_file_path, force)
        RepoSettings.__init_repo_file(self.user_settings.dipr_dep_template_file_path, self.dipr_dep_file_path, force)
        RepoSettings.__init_repo_file(self.user_settings.dipr_sub_template_file_path, self.dipr_sub_file_path, force)

    def resolve_repos(self, reset=False):

        if self.resolved and not reset:
            return

        self.root_repo_handler = resolve_repo_handler(full_repo_path=self.root_repo_path)
        self.resolved_dependencies = self.__resolve_repo(self.dependencies)
        self.resolved_subrepos = self.__resolve_repo(self.subrepos)

        self.resolved = True

    def save_sources(self):
        self.sources.save()

    def save_dependencies(self):
        self.dependencies.save()

    def save_subrepos(self):
        self.subrepos.save()

    def save_repo_files(self):
        self.sources.save()
        self.dependencies.save()
        self.subrepos.save()

    def __resolve_repo(self, repos):
        resolved = []

        for k, r in repos.items():
            if r and r.src_key in self.sources:
                resolved.append(DiprResolvedRepo(self.root_repo_path, self.sources[r.src_key], r))
            else:
                Console.warning("Could not find source " + r.src_key + " for repo " + r.repo_key + ".")

        return resolved
