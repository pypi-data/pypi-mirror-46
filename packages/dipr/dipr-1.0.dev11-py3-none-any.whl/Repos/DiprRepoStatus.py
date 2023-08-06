
class DiprRepoStatus(object):

    def __init__(self, resolved_repo):
        self.__resolved_repo = resolved_repo

        self.have_handler = False
        self.path_exists = False
        self.is_valid = False
        self.is_empty = False
        self.current_branch = None
        self.on_default_branch = False
        self.current_tags = []
        self.current_version = None
        self.is_at_tip = False
        self.has_changes = False
        self.at_correct_version = False

        self.__evaluate()

    def __evaluate(self):
        self.have_handler = bool(self.__resolved_repo.handler)

        if not self.have_handler:
            return

        self.path_exists = self.__resolved_repo.handler.exists

        if not self.path_exists:
            return

        self.is_valid = self.__resolved_repo.handler.is_valid()

        if not self.is_valid:
            return

        self.has_changes = self.__resolved_repo.handler.has_changes()

        self.is_empty = self.__resolved_repo.handler.is_empty()

        if self.is_empty:
            return

        self.current_branch = self.__resolved_repo.handler.get_current_branch()
        self.on_default_branch = self.__resolved_repo.handler.is_on_default_branch()
        self.current_tags = self.__resolved_repo.handler.get_current_tags()
        self.current_version = self.__resolved_repo.handler.get_current_revision()
        self.is_at_tip = self.__resolved_repo.handler.is_current_revision_tip()

        at_correct_version = False

        if self.__resolved_repo.version_is_tip:
            at_correct_version = self.is_at_tip and self.on_default_branch
        elif self.__resolved_repo.version_is_revision and self.current_version:
            rev = self.__resolved_repo.revision
            at_correct_version = self.current_version == rev \
                                 or rev.startswith(self.current_version) \
                                 or self.current_version.startswith(rev)
        elif self.__resolved_repo.version_is_tag and self.current_tags:
            at_correct_version = self.__resolved_repo.tag in self.current_tags
        elif self.__resolved_repo.version_is_branch and self.current_branch:
            at_correct_version = self.is_at_tip and self.current_branch == self.__resolved_repo.branch

        self.at_correct_version = at_correct_version

    def summary_string(self):
        repo_path = self.__resolved_repo.repo_path
        output = str(repo_path) + ", "

        error = True

        if not self.have_handler:
            output += "Could not determine a revision control protocol."
        elif not self.path_exists:
            output += "Path does not exist.  Has it been pulled?"
        elif not self.is_valid:
            output += "Path is not valid for the " + self.__resolved_repo.protocol + " protocol."
        elif self.is_empty:
            output += "The repo is valid but it is empty."
        else:
            error = False

        if error:
            if self.has_changes:
                return "[#] " + output + " (Has Changes)."
            else:
                return "[X] " + output

        current_branch = self.current_branch
        current_tags = self.current_tags
        actual_version = self.current_version

        if not current_branch:
            current_branch = ""

        if not actual_version:
            actual_version = "???"

        if self.is_at_tip:
            if current_branch:
                tip_version = "tip, " + current_branch
            else:
                tip_version = "tip"

            actual_version = tip_version + " (" + actual_version + ")"

        if current_tags:
            actual_version = ", ".join(current_tags) + " [" + actual_version + "]"

        defined_version = self.__resolved_repo.long_version

        output += "at " + actual_version + " => " + defined_version

        if self.has_changes:
            status_code = "#"
        elif not self.at_correct_version:
            status_code = "@"
        else:
            status_code = " "

        output = "[" + status_code + "] " + output

        return output

    def __str__(self):
        return self.summary_string()