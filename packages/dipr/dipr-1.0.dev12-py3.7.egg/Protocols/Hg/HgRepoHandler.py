import subprocess

from Utilities.Console import Console

from Protocols.AbstractRepoHandler import AbstractRepoHandler

from . import HgCommander


class HgRepoHandler(AbstractRepoHandler):

    HG_ID = "HG"

    def __init__(self, resolved_repo=None, full_repo_path=None):
        super().__init__(resolved_repo=resolved_repo, full_repo_path=full_repo_path)

        self.__hg = HgCommander(str(self.full_repo_path))

    def __check_is_hg_dir(self, warn=True):
        """
        Check to see if the resolved repo is a git directory.
        :param warn: If set to true, issues a warning
        :return: True if it is a git dir, otherwise false.  Issues warning if warn is true.
        """
        if not self.__hg.is_hg_dir:
            if warn:
                Console.warning("Path: " + str(self.resolved_repo.repo_path) + "is not an hg directory.")
            return False

        return True

    @staticmethod
    def have_hg():
        return bool(HgRepoHandler.get_hg_version_string())

    @staticmethod
    def get_hg_version_string():
        try:
            result = subprocess.run(['hg', '--version'], stdout=subprocess.PIPE)
            return result.stdout.decode().split('\n')[0]
        except:
            return ""

    @staticmethod
    def is_hg_dir(full_repo_path):
        try:
            return HgRepoHandler(full_repo_path=full_repo_path).__check_is_hg_dir()
        except:
            return False


    # region Abstract Protocol Implementations

    def is_valid(self):
        return HgRepoHandler.is_hg_dir(self.full_repo_path)

    def is_empty(self):
        return self.__hg.is_empty()

    def pull(self):
        """
        Perform a repo pull for the specified resolved repo.
        """

        if not self._have_resolved_repo:
            Console.error("Cannot pull without a resolved repo object.")
            return

        if not super()._repo_path_exists or super()._repo_path_empty:
            self.__hg.clone(self.resolved_repo.url)
            return

        if not self.__check_is_hg_dir():
            return

        self.__hg.pull()

    def update(self, reset):
        """
        Perform a repo update for the specified resolved repo.
        :param reset: If true, perform a reset of the repo.
        """
        if not self._have_resolved_repo:
            Console.error("Cannot update without a resolved repo object.")
            return

        if not super()._repo_path_exists or super()._repo_path_empty:
            Console.warning("Repo " + str(self.resolved_repo.repo_path) + " is empty.  Pull first.")
            return

        if not self.__check_is_hg_dir():
            return

        if self.resolved_repo.version_is_revision:
            rev = self.resolved_repo.revision
        elif self.resolved_repo.version_is_tag:
            rev = self.resolved_repo.tag
        elif self.resolved_repo.version_is_branch:
            rev = self.resolved_repo.branch
        else:
            rev = "default"

        self.__hg.update(rev=rev, clean=reset)

    def get_current_revision(self):
        """
        Return the current revision ID for the repo.
        :return: The current revision ID.
        """
        return self.__hg.get_current_revision()

    def get_current_tags(self):
        return self.__hg.get_current_tags()

    def get_latest_tags(self, branch=None):
        """
        Return the latest tag on the repo.
        :return: The latest available tag or None if there is no tag.
        """
        return self.__hg.get_latest_tags(branch)

    def is_current_revision_tip(self):
        return self.__hg.is_current_revision_tip()

    def get_current_branch(self):
        return self.__hg.get_current_branch()

    def is_on_default_branch(self):
        return self.__hg.is_on_default_branch()

    def has_changes(self):
        return self.__hg.has_changes()

    def discard(self):
        self.__hg.update(clean=True)
        self.__hg.purge()

    def commit(self, message, add_remove):
        self.__hg.commit(message, add_remove)

    def tag(self, tag, message):
        self.__hg.tag(tag, message)

    def push(self, force):
        self.__hg.push(force)

    def is_tracked(self, file):
        """
        Checks if a file is already tracked by revision control.
        :param file: The path to a file to check.
        :return: True if it is tracked (in revision control) else False
        """
        return self.__hg.is_tracked(file)

    def add(self, file):
        """
        Add the provided file to the revision control system.
        :param file: The path to a file to add/stage to in revision control.
        """
        self.__hg.add(file)

    def remove(self, file):
        """
        Remove the provided file from the revision control system.
        :param file: The path to a file to remove from disk and revision control.
        """
        return self.__hg.remove(file)

    # endregion
