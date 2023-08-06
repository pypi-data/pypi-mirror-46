import subprocess

from Utilities.Console import Console

from Protocols.AbstractRepoHandler import AbstractRepoHandler

from . import GitCommander


class GitRepoHandler(AbstractRepoHandler):

    GIT_ID = "GIT"

    @staticmethod
    def __split_remote(default_remote, branch):
        """
        The branch may be a remote/branch combination.  Split them or use the default_remote if none is specified.
        :param default_remote: The default remote to use if none is provided in branch.
        :param branch: The branch that may also contain a remote.
        :return: A list with a remote and branch.
        """
        remote = default_remote
        split = []

        if "/" in branch:
            split = list(map(lambda x: x.trim(), branch.split("/")))

        if "\\" in branch:
            split = list(map(lambda x: x.trim(), branch.split("\\")))

        if len(split) == 2:
            remote = split[0]
            branch = split[1]

        return [remote, branch]

    @staticmethod
    def have_git():
        return bool(GitRepoHandler.get_git_version_string())

    @staticmethod
    def get_git_version_string():
        try:
            result = subprocess.run(['git', '--version'], stdout=subprocess.PIPE)
            return result.stdout.decode().split('\n')[0]
        except:
            return ""

    @staticmethod
    def is_git_dir(full_repo_path):
        try:
            return GitRepoHandler(full_repo_path=full_repo_path).__check_is_git_dir()
        except:
            return False

    def __init__(self, resolved_repo=None, full_repo_path=None):
        """
        Initialize the base repo.
        :param resolved_repo: The previously resolved repo the git client will act upon.
        """
        super().__init__(resolved_repo=resolved_repo, full_repo_path=full_repo_path)

        self.__git = GitCommander(self.full_repo_path)

    def __check_is_git_dir(self, warn=True):
        """
        Check to see if the resolved repo is a git directory.
        :param warn: If set to true, issues a warning
        :return: True if it is a git dir, otherwise false.  Issues warning if warn is true.
        """
        if not self.__git.is_git_dir:
            if warn:
                Console.warning("Path: " + str(self.resolved_repo.repo_path) + "is not a git directory.")
            return False

        return True

    def __parse_revision(self):
        """
        Parse the revision information from resolved repo to come up with a git providable revision string.
        :return: A string that may be passed to the appropriate git call.
        """

        remote = ""

        if self.resolved_repo.version_is_tag:
            revision = "tags/" + self.resolved_repo.tag
        elif self.resolved_repo.version_is_branch:
            [remote, revision] = GitRepoHandler.__split_remote(remote, self.resolved_repo.branch)
        elif self.resolved_repo.version_is_revision:
            if self.resolved_repo.version_is_tip:
                revision = "master"
            else:
                revision = self.resolved_repo.revision
        else:
            revision = "master"

        return [remote, revision]

    # region Abstract Protocol Implementations

    def is_valid(self):
        return GitRepoHandler.is_git_dir(self.full_repo_path)

    def is_empty(self):
        return self.__git.is_empty()

    def pull(self):
        """
        Perform a repo pull for the specified resolved repo.
        """
        if not self._have_resolved_repo:
            Console.error("Cannot pull without a resolved repo object.")
            return

        if not super()._repo_path_exists or super()._repo_path_empty:
            self.__git.clone(self.resolved_repo.url)
            return

        if not self.__check_is_git_dir():
            return

        [remote, _] = self.__parse_revision()

        self.__git.fetch(remote)

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

        if not self.__check_is_git_dir():
            return

        [remote, revision] = self.__parse_revision()

        if reset:
            self.__git.reset(remote, revision)

        self.__git.checkout(remote, revision)

        if not self.resolved_repo.version_is_revision and not self.resolved_repo.version_is_tag:
            self.__git.pull()

        Console.info(self.__git.status())

    def get_current_revision(self):
        return self.__git.get_current_revision()

    def get_current_tags(self):
        return self.__git.get_current_tags()

    def get_latest_tags(self, branch=None):
        return self.__git.get_latest_tags(branch)

    def is_current_revision_tip(self):
        return self.__git.is_current_revision_tip()

    def get_current_branch(self):
        return self.__git.get_current_branch()

    def is_on_default_branch(self):
        return self.__git.is_on_default_branch()

    def has_changes(self):
        return self.__git.has_changes()

    def discard(self):
        self.__git.discard()
        pass

    def commit(self, message, add_remove):
        self.__git.commit(message, add_remove)
        pass

    def tag(self, tag, message):
        self.__git.tag(tag, message)

    def push(self, force):
        self.__git.push(force)

    def is_tracked(self, file):
        """
        Checks if a file is already tracked by revision control.
        :param file: The path to a file to check.
        :return: True if it is tracked (in revision control) else False
        """
        return self.__git.file_status(file) is None

    def add(self, file):
        """
        Add the provided file to the revision control system.
        :param file: The path to a file to add/stage to in revision control.
        """
        self.__git.add(file)

    def remove(self, file):
        """
        Remove the provided file from the revision control system.
        :param file: The path to a file to remove from disk and revision control.
        """
        self.__git.remove(file)

    # endregion
