from pathlib import Path

from Protocols.ProtocolHelper import resolve_repo_handler
from Repos.DiprRepoStatus import DiprRepoStatus


class DiprResolvedRepo(object):

    def __init__(self, root_repo_path, source, repo):
        if repo.repo_path.is_absolute():
            self.__full_repo_path = repo.repo_path
        else:
            self.__full_repo_path = Path(root_repo_path, repo.repo_path)

        self.__source = source
        self.__repo = repo

    @property
    def src_key(self):
        return self.__source.src_key

    @property
    def repo_key(self):
        return self.__repo.repo_key

    @property
    def url(self):
        return self.__source.url

    @property
    def protocol(self):
        return self.__source.protocol.upper()

    @property
    def repo_path(self):
        return self.__repo.repo_path

    @property
    def full_repo_path(self):
        return self.__full_repo_path

    @property
    def version(self):
        return self.__repo.version_string

    @property
    def long_version(self):
        return self.__repo.long_version_string

    @property
    def tag(self):
        return self.__repo.tag

    @property
    def version_is_tag(self):
        return self.__repo.have_tag

    @property
    def branch(self):
        return self.__repo.branch

    @property
    def version_is_branch(self):
        return self.__repo.have_branch

    @property
    def revision(self):
        return self.__repo.revision

    @property
    def version_is_revision(self):
        return self.__repo.have_revision

    @property
    def version_is_tip(self):
        return self.__repo.use_tip

    @property
    def handler(self):
        return resolve_repo_handler(self, self.full_repo_path)

    def set_tag(self, tag):
        self.__repo.set_tag(tag)

    def set_revision(self, rev):
        self.__repo.set_revision(rev)

    def set_branch(self, branch):
        self.__repo.set_branch(branch)

    def set_tip(self):
        self.__repo.set_tip()

    def __str__(self):
        return str(self.repo_key) + " => [" + self.protocol.upper() + "] " + self.src_key + ": " + self.url + \
               " (" + self.version + ")"

    @property
    def status(self):
        return DiprRepoStatus(self)

