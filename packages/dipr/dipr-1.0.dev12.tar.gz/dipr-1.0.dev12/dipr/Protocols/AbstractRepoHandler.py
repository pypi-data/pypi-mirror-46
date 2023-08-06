import os

from abc import ABC, abstractmethod


class AbstractRepoHandler(ABC):
    """Specify the mandatory functions for a protocol provider."""

    def __init__(self, resolved_repo=None, full_repo_path=None):
        """
        Initialize the resolve repo variable.
        :param resolved_repo: A previously resolved repo to operate on.
        """
        self.resolved_repo = resolved_repo
        self.full_repo_path = full_repo_path

        if self.resolved_repo:
            self.full_repo_path = self.resolved_repo.full_repo_path

    @property
    def _have_resolved_repo(self):
        """
        Returns true if a resolved repo object was provided.
        :return:
        """
        return self.resolved_repo

    @property
    def _repo_path_exists(self):
        """
        Check if the full repo path specified in resolve repo exists.
        :return: True if the full repo path exists else False.
        """
        return self.full_repo_path.is_dir()

    @property
    def _repo_path_empty(self):
        """
        Check if the full repo path specified in resolve repo is empty.
        :return: True if the full repo path is empty, else False.
        """
        return not bool(os.listdir(str(self.full_repo_path)))

    @property
    def exists(self):
        """
        Check to see if the repo path exists.
        :return: True if the path already exists, False otherwise.
        """
        return self._repo_path_exists and not self._repo_path_empty

    @abstractmethod
    def is_valid(self):
        """
        Check to see if the path is valid for the revision control protocol.
        :return: True if the repo is valid else False
        """
        raise NotImplementedError

    @abstractmethod
    def is_empty(self):
        """
        Return true if the repo is valid but has no commits.
        :return: True if there are no commits in the repo, otherwise False.
        """
        raise NotImplementedError

    @abstractmethod
    def pull(self):
        """
        Implement the logic necessary to perform the pull command.
        :param arguments: Command line arguments from the pull command.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, reset):
        """
        Implement the logic necessary to perform the update command.
        :param reset: If true, perform a reset of the repo.
        """
        raise NotImplementedError

    @abstractmethod
    def get_current_revision(self):
        """
        Return the current revision ID for the repo.
        :return: The current revision ID.
        """
        raise NotImplementedError

    @abstractmethod
    def is_current_revision_tip(self):
        """
        Check if the current revision is the tip of its branch.
        :return: True if it is the tip, else false.
        """
        raise NotImplementedError

    @abstractmethod
    def get_current_tags(self):
        """
        Return a list of tags of the current revision else an empty list of none.
        :return: A list of tags for the revision or an empty array.
        """
        raise NotImplementedError

    @abstractmethod
    def get_latest_tags(self, branch=None):
        """
        Return the latest tag on the repo.
        :return: The latest available tag or None if there is no tag.
        """
        raise NotImplementedError

    @abstractmethod
    def get_current_branch(self):
        """
        Return the current branch if one can be identified.
        :return: Returns the current branch if one can be identified otherwise returns None.
        """
        raise NotImplementedError

    @abstractmethod
    def is_on_default_branch(self):
        """
        Check if the current branch is the default branch.
        :return: True if the current branch is default, False if no branch or a different branch.
        """
        raise NotImplementedError

    @abstractmethod
    def has_changes(self):
        """
        Check if the repo has changes that have not been committed.
        :return: True if there are uncommitted changes, else False
        """
        raise NotImplementedError

    @abstractmethod
    def discard(self):
        """
        Discard any uncommitted changes in the repo.
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    def commit(self, message, add_remove):
        """
        Commit changes in this repo with the provided commit message.
        :param message: The message to apply to the commit.
        :param add_remove: If true, add any files that are not added and remove any missing files.
        """
        raise NotImplementedError

    @abstractmethod
    def tag(self, tag, message):
        """
        Tag the repo with the provided tag name and apply a message to the commit if any.
        :param tag: The name of the tag to apply.
        :param message: A message to go with the tag commit.
        """
        raise NotImplementedError

    @abstractmethod
    def push(self, force):
        """
        Push the repo back to its original remote/server.
        """
        raise NotImplementedError

    @abstractmethod
    def is_tracked(self, file):
        """
        Checks if a file is already tracked by revision control.
        :param file: The path to a file to check.
        :return: True if it is tracked (in revision control) else False
        """
        raise NotImplementedError

    @abstractmethod
    def add(self, file):
        """
        Add the provided file to the revision control system.
        :param file: The path to a file to add/stage to in revision control.
        """
        raise NotImplementedError

    @abstractmethod
    def remove(self, file):
        """
        Remove the provided file from the revision control system.
        :param file: The path to a file to remove from disk and revision control.
        """
        raise NotImplementedError
