
import stat
import shutil

from git import *

from Utilities.Console import Console


class GitSubmoduleImporter(object):

    def __init__(self, full_repo_path):
        self.full_repo_path = full_repo_path

    @property
    def is_git_repo(self):
        try:
            _ = self.git_repo
            return True
        except InvalidGitRepositoryError:
            return False

    @property
    def have_submodules(self):
        return len(self.git_repo.submodules) > 0

    @property
    def git_repo(self):
        return Repo(self.full_repo_path)

    @staticmethod
    def __get_key_from_name(path):
        path = os.path.normpath(path)
        segments = path.split(os.sep)

        if segments and len(segments) > 0:
            return str(segments[-1])
        else:
            return None

    def import_into(self, sources, depends, force):
        """
        Iterate over submodule entries and add them as appropriate to source and depends.
        :param source: An instance of DipSources to add the sources into.
        :param depends: An instance of DipDependencies to add the entries into.
        """

        if not self.is_git_repo:
            return 0

        if not self.have_submodules:
            return 0

        repo = self.git_repo

        import_count = 0

        for sm in repo.submodules:
            key = GitSubmoduleImporter.__get_key_from_name(sm.name)

            if not key:
                Console.warning("Could not parse key for: " + sm.name + ". Ignoring.")
                continue

            url = sm.url
            path = os.path.normpath(sm.path)
            sm_full_path = os.path.join(self.full_repo_path, path)

            try:
                sm_repo = Repo(sm_full_path)
                rev = sm_repo.git.describe("--always")
            except GitCommandError as e:
                Console.warning("Could not retrieve revision information for submodule: " + path)
                Console.info("Error: " + str(e))
                continue
            except InvalidGitRepositoryError as e:
                Console.warning("The submodule was invalid.  Could not get revision information: " + path)
                Console.info("Error: " + str(e))
                continue

            Console.print("Importing submodule: " + key)

            sources.add(key.upper(), protocol="GIT", url=url, replace=force)
            depends.add(path, src_key=key, revision=rev, replace=force)

            import_count += 1

        return import_count

    @staticmethod
    def rm_r(path):
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path, onerror=GitSubmoduleImporter.remove_readonly)
        elif os.path.exists(path):
            os.remove(path)

    @staticmethod
    def remove_readonly(func, path, _):
        "Clear the readonly bit and reattempt the removal"
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def clean(self, force):
        """
        Clean out the existing submodule information.

        It is not intuitive.  See here for answers:
        https://stackoverflow.com/questions/1260748/how-do-i-remove-a-submodule/36593218#36593218
        :param force:  If true, pass force flags to the various calls that support it.
        :return:
        """
        if not self.is_git_repo:
            Console.error("Cannot import submodules or clean them if the path is not a git repo.")
            return

        if not self.have_submodules:
            return

        repo = self.git_repo

        for sm in repo.submodules:
            path = os.path.normpath(sm.path)

            Console.print("Cleaning submodule: " + path)

            try:
                if force:
                    repo.git.submodule("deinit", "-f", path)
                else:
                    repo.git.submodule("deinit", path)
            except GitCommandError as e:
                Console.error("Could not deinit submodule " + path + ". Error: " + str(e))
                continue

            try:
                module_path = os.path.join(self.full_repo_path, ".git", "modules", path)
                GitSubmoduleImporter.rm_r(module_path)
                #module_paths.append(module_path)
            except Exception as e:
                Console.error("Failed to cleanup the module directory: " + str(e))
                continue

            try:
                if force:
                    repo.git.rm("-f", path)
                else:
                    repo.git.rm(path)
            except GitCommandError as e:
                Console.error("Could not remove final submodule reference: " + str(e))

        repo.close()
