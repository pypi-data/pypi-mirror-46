
from Utilities.Console import Console

from Protocols.Hg import hglib
from .hglib.error import *


class HgCommander(object):

    def __init__(self, full_repo_path):
        self.full_repo_path = full_repo_path

    @property
    def __hg_repo(self):
        return hglib.open(self.full_repo_path)

    @staticmethod
    def __b(value):
        """
        Because Hg Lib is setup to only work with binary encoded strings(8 bit ASCII) and is TERRIBLE at sanitizing
        its inputs, this function is necessary to do that for it.  This also makes unicode out of the question for
        HG repos.
        :param value: A value to be binarized.
        :return:
        """
        if isinstance(value, bytes):
            return value

        return str(value).encode('latin-1')

    @property
    def is_hg_dir(self):
        try:
            self.__hg_repo.status()
            return True
        except Exception as e:
            return False

    def is_empty(self):
        try:
            output = self.__hg_repo.identify(num=True).decode().strip()

            if not output:
                return True

            output = output.replace("+", "")

            return int(output) < 0
        except CommandError as e:
            Console.warning("Command error during commit check: " + str(e))
        except ServerError as e:
            Console.warning("Server error during commit check: " + str(e))

        return False

    def clone(self, url):
        try:
            hglib.clone(HgCommander.__b(url), dest=HgCommander.__b(self.full_repo_path))
        except CommandError as e:
            Console.warning("Command error during clone: " + str(e))
        except ServerError as e:
            Console.warning("Server error during clone: " + str(e))

    def pull(self):
        try:
            self.__hg_repo.pull()
        except CommandError as e:
            Console.warning("Command error during pull: " + str(e))
        except ServerError as e:
            Console.warning("Server error during pull: " + str(e))

    def status(self):
        try:
            return self.__hg_repo.status()
        except CommandError as e:
            Console.warning("Command error during status: " + str(e))
        except ServerError as e:
            Console.warning("Server error during status: " + str(e))

    def update(self, clean=False, rev=None):
        try:
            if rev:
                self.__hg_repo.update(rev=HgCommander.__b(rev), clean=clean)
            else:
                self.__hg_repo.update(clean=clean)
        except CommandError as e:
            Console.warning("Command error during update: " + str(e))
        except ServerError as e:
            Console.warning("Server error during update: " + str(e))

    def purge(self):
        try:
            self.__hg_repo.purge()
        except CommandError as e:
            Console.warning("The purge command may be unavailable.  Discard will not fully clean the repo.")
            Console.info("Exception: " + str(e))
        except ServerError as e:
            Console.warning("Server error during update: " + str(e))

    def discard(self):
        try:
            self.__hg_repo.update(clean=True)
        except CommandError as e:
            Console.warning("Command error during discard: " + str(e))
        except ServerError as e:
            Console.warning("Server error during discard: " + str(e))

    def get_current_revision(self):
        try:
            revisions = self.__hg_repo.identify().decode().split(" ")
            return revisions[0].strip().replace("+", "")
        except CommandError as e:
            Console.warning("Command error while getting revision ID: " + str(e))
        except ServerError as e:
            Console.warning("Server error while getting revision ID: " + str(e))

        return None

    def get_current_tags(self):
        try:
            tags = self.__hg_repo.identify(tags=True).decode().strip().split(" ")
            if "tip" in tags:
                tags.remove("tip")
            if "" in tags:
                tags.remove("")
            return tags
        except CommandError as e:
            Console.warning("Command error while getting current tag: " + str(e))
        except ServerError as e:
            Console.warning("Server error while getting current tag: " + str(e))

        return None

    def get_latest_tags(self, branch):
        try:
            if not branch:
                branch = "default"
            tags = self.__hg_repo.log(revrange=HgCommander.__b("branch(" + branch + ") and tag()"), template=HgCommander.__b("{tags} "))
            tags = tags.decode().strip().split(" ")
            tags.reverse()
            if tags and "tip" in tags:
                tags.remove("tip")
            if tags and "" in tags:
                tags.remove("")
            return tags
        except CommandError as e:
            Console.warning("Command error getting latest tag: " + str(e))
        except ServerError as e:
            Console.warning("Server error getting latest tag: " + str(e))

        return None

    def __get_tip_rev_for_branch(self, branch):
        try:
            tip = self.__hg_repo.heads(branch=HgCommander.__b(branch), template=HgCommander.__b("{node|short}"))
            if tip:
                return tip.decode().strip()
            else :
                return None
        except CommandError as e:
            Console.warning("Command error while getting tip of branch (" + branch + "): " + str(e))
        except ServerError as e:
            Console.warning("Server error while getting tip of branch (" + branch + "): " + str(e))

        return None

    def is_current_revision_tip(self):
        current_branch = self.get_current_branch()

        if not current_branch:
            return False

        current_rev = self.get_current_revision()

        if not current_rev:
            return False

        tip_rev = self.__get_tip_rev_for_branch(current_branch)

        if not tip_rev:
            return False

        return current_rev == tip_rev

    def get_current_branch(self):
        try:
            revisions = self.__hg_repo.identify(branch=True).decode().split(" ")
            return revisions[0].strip()
        except CommandError as e:
            Console.warning("Command error while getting branch: " + str(e))
        except ServerError as e:
            Console.warning("Server error while getting branch: " + str(e))

        return None

    def is_on_default_branch(self):
        branch = self.get_current_branch()

        return branch and branch == "default"

    def has_changes(self):
        try:
            changes = self.__hg_repo.status(modified=True,added=True,removed=True,deleted=True,unknown=True)
            return bool(changes)
        except CommandError as e:
            Console.warning("Command error while checking for changes: " + str(e))
        except ServerError as e:
            Console.warning("Server error while checking for changes: " + str(e))
        return False

    def is_tracked(self, file):
        try:
            status = self.__hg_repo.status(include=[HgCommander.__b(file)])

            if status and len(status) > 0:
                return str(status[0]).startswith("A")
        except CommandError as e:
            Console.warning("Command error during file status: " + str(e))
        except ServerError as e:
            Console.warning("Server error during file status: " + str(e))

        return False

    def add(self, file):
        try:
            self.__hg_repo.add(HgCommander.__b(file))
        except CommandError as e:
            Console.warning("Command error during add of file " + file + ": " + str(e))
        except ServerError as e:
            Console.warning("Server error during add of file " + file + ": " + str(e))

    def remove(self, file):
        try:
            self.__hg_repo.remove(HgCommander.__b(file))
        except CommandError as e:
            Console.warning("Command error during remove of file " + file + ": " + str(e))
        except ServerError as e:
            Console.warning("Server error during remove of file " + file + ": " + str(e))

    def commit(self, message, add_remove):
        try:
            self.__hg_repo.commit(message=HgCommander.__b(message), addremove=add_remove)
        except CommandError as e:
            Console.warning("Command error during commit: " + e.out.decode().strip())
        except ServerError as e:
            Console.warning("Server error during commit: " + str(e))

    def tag(self, name, message):
        try:
            self.__hg_repo.tag(HgCommander.__b(name), message=HgCommander.__b(message))
        except CommandError as e:
            Console.warning("Command error during tag: " + str(e))
        except ServerError as e:
            Console.warning("Server error during tag: " + str(e))

    def push(self, force=False):
        try:
            self.__hg_repo.push(force=force)
        except CommandError as e:
            Console.warning("Command error during push: " + str(e))
        except ServerError as e:
            Console.warning("Server error during push: " + str(e))
