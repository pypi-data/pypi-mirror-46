
import os

from Utilities.Console import Console

from Protocols.ProtocolHelper import resolve_repo_handler


class HgGuestRepoImporter(object):

    GRMAPPING_FILE = ".hggrmapping"
    GUESTREPO_FILE = ".hgguestrepo"

    def __init__(self, full_repo_path):
        self.full_repo_path = full_repo_path

    @property
    def have_guestrepo_files(self):
        return False

    @property
    def grmap_file(self):
        return os.path.join(self.full_repo_path,  HgGuestRepoImporter.GRMAPPING_FILE)

    @property
    def guestrepo_file(self):
        return os.path.join(self.full_repo_path, HgGuestRepoImporter.GUESTREPO_FILE)

    @staticmethod
    def __safe_remove(repo, file):
        try:
            if os.path.isfile(file):
                if repo.is_tracked(file):
                    repo.remove(file)
                else:
                    os.remove(file)
        except Exception as e:
            Console.warning("Could not remove file " + file)
            Console.info("Error: " + str(e))

    def import_into(self, sources, depends, force):
        """
        Iterate over .hggrmapping sources and add them into the DipSources dictionary.
        Iterate over .hgguestrepo entries and add then to the DipDependencies dictionary.
        :param sources: An instance of DipSources to add the sources into.
        :param depends: An instance of DipDependencies to add the entries into.
        """

        grmap_file = self.grmap_file
        guestrepo_file = self.guestrepo_file

        if not os.path.isfile(grmap_file):
            Console.error("HG guest repo mapping file not found: " + grmap_file)
            return 0

        if not os.path.isfile(guestrepo_file):
            Console.error("HG guest repo file not found: " + guestrepo_file)
            return 0

        count = HgGuestRepoImporter.__import_grmapping(grmap_file, sources, force)

        Console.print("Imported " + str(count) + " HG guest repo sources.")

        count = HgGuestRepoImporter.__import_guestrepo(guestrepo_file, depends, force)

        Console.print("Imported " + str(count) + " HG guest repo dependencies.")

        return count

    def clean(self, _):
        repo = resolve_repo_handler(full_repo_path=self.full_repo_path)

        if repo is None:
            return

        grmap_file = self.grmap_file
        guestrepo_file = self.guestrepo_file

        Console.print("Removing: " + grmap_file)
        HgGuestRepoImporter.__safe_remove(repo, grmap_file)

        Console.print("Removing: " + guestrepo_file)
        HgGuestRepoImporter.__safe_remove(repo, guestrepo_file)

    @staticmethod
    def __import_grmapping(grmap_file, sources, force):
        count = 0

        with open(grmap_file, 'r') as file:
            for line in file:
                if "#" in line:
                    continue

                line = line.strip()
                parts = line.split("=")

                if not parts or len(parts) < 2:
                    continue

                key = parts[0].strip()
                url = parts[1].strip()

                sources.add(key.upper(), protocol="HG", url=url, replace=force)
                count += 1

        return count

    @staticmethod
    def __import_guestrepo(guestrepo_file, depends, force):
        count = 0

        with open(guestrepo_file, 'r') as file:
            for line in file:
                if "#" in line:
                    continue

                line = line.strip()
                parts = line.split("=")

                if not parts or len(parts) < 2:
                    continue

                repo_path = parts[0].strip()
                tag_and_version = parts[1]

                parts = tag_and_version.split()

                if not parts or len(parts) < 2:
                    continue

                key = parts[0].strip()
                revision = parts[1].strip()

                if revision is not "*" and revision.lower() is not "tip":
                    depends.add(repo_path, src_key=key, tag=revision, replace=force)
                else:
                    depends.add(repo_path, src_key=key, revision=revision, replace=force)

                count += 1

        return count
        pass


