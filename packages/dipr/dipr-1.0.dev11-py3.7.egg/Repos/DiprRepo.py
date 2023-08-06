
from pathlib import Path, PurePath

from Repos.YamlDict import YamlDict


class DipRepo(YamlDict):

    SRC_KEY_KEY = "KEY"
    REVISION_KEY = "REVISION"
    TAG_KEY = "TAG"
    BRANCH_KEY = "BRANCH"

    def __init__(self, repo_path, values=None, src_key=None, revision=None, tag=None, branch=None):
        super().__init__(PurePath(repo_path).as_posix(), values=values)

        if src_key:
            self[DipRepo.SRC_KEY_KEY] = str(src_key).strip().upper()

        if revision:
            if revision.lower() is not "tip" and revision is not "*":
                self[DipRepo.REVISION_KEY] = str(revision).strip()
        elif tag:
            self[DipRepo.TAG_KEY] = str(tag).strip()
        elif branch:
            self[DipRepo.BRANCH_KEY] = str(branch).strip()

    def __clear_revision_info(self):
        if DipRepo.REVISION_KEY in self:
            del self[DipRepo.REVISION_KEY]

        if DipRepo.TAG_KEY in self:
            del self[DipRepo.TAG_KEY]

        if DipRepo.BRANCH_KEY in self:
            del self[DipRepo.BRANCH_KEY]

    @property
    def repo_key(self):
        return super().yaml_root_key

    @property
    def repo_path(self):
        return Path(super().yaml_root_key)

    @property
    def src_key(self):
        return self[DipRepo.SRC_KEY_KEY]

    @property
    def revision(self):
        return self[DipRepo.REVISION_KEY]

    @property
    def tag(self):
        return self[DipRepo.TAG_KEY]

    @property
    def branch(self):
        return self[DipRepo.BRANCH_KEY]

    @property
    def have_tag(self):
        return bool(self.tag)

    @property
    def have_branch(self):
        return bool(self.branch)

    @property
    def have_revision(self):
        return bool(self.revision)

    @property
    def use_tip(self):
        return bool(not self.tag and not self.branch and not self.revision) \
               or (self.have_revision and (self.revision.lower() == "tip" or self.revision == "*"))

    def set_tag(self, tag):
        self.__clear_revision_info()
        self[DipRepo.TAG_KEY] = tag

    def set_revision(self, rev):
        self.__clear_revision_info()
        self[DipRepo.REVISION_KEY] = rev

    def set_branch(self, branch):
        self.__clear_revision_info()
        self[DipRepo.BRANCH_KEY] = branch

    def set_tip(self):
        self.__clear_revision_info()

    @property
    def version_string(self):
        return self.get_version_string(False)

    @property
    def long_version_string(self):
        return self.get_version_string(True)

    def get_version_string(self, long=False):
        if self.have_tag:
            if long:
                return "Tag: " + self.tag
            else:
                return "#" + self.tag
        elif self.have_branch:
            if long:
                return "tip, " + self.branch
            else:
                return "@" + self.branch
        elif self.have_revision:
            return self.revision
        else:
            if long:
                return "tip, default"
            else:
                return "*"
