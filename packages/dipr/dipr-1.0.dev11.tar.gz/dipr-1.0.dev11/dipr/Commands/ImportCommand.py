import collections
import os

from Utilities.Console import Console

from Arguments.ImportArguments import ImportArguments
from Commands.DiprCommandBase import DiprCommandBase

from Protocols.Hg.HgGuestRepoImporter import HgGuestRepoImporter
from Protocols.Git.GitSubmoduleImporter import GitSubmoduleImporter

import gitlab


class ImportCommand(DiprCommandBase):

    def __init__(self, user_settings):
        super().__init__(user_settings)

    def execute(self, arguments):
        repo_settings = super()._open_repo(arguments)
        import_args = arguments.import_command

        if not repo_settings.is_initialized:
            Console.error("Repo " + repo_settings.root_repo_path + " is not initialized.")
            return

        source = import_args.source.lower()

        import_count = 0

        if source == ImportArguments.GUESTREPO_SOURCE:
            hg_importer = HgGuestRepoImporter(repo_settings.root_repo_path)
            import_count = hg_importer.import_into(repo_settings.sources, repo_settings.dependencies, import_args.force)

            if arguments.import_command.clean:
                hg_importer.clean(arguments.import_command.clean_yes)

        elif source == ImportArguments.SUBMODULES_SOURCE:
            sm_importer = GitSubmoduleImporter(repo_settings.root_repo_path)
            import_count = sm_importer.import_into(repo_settings.sources, repo_settings.dependencies, import_args.force)

            if arguments.import_command.clean:
                sm_importer.clean(arguments.import_command.clean_yes)

        elif source == ImportArguments.GITLAB_SOURCE:
            import_count = ImportCommand.__import_gitlab(import_args, repo_settings)

        else:
            Console.error("Import source must be one of: " + ", ".join(ImportArguments.IMPORT_SOURCES))

        if import_count > 0:
            repo_settings.resolve_repos(reset=True)
            repo_settings.save_repo_files()
            Console.print("Imported " + str(import_count) + " repos.")
        else:
            Console.print("No repos imported.")

    @staticmethod
    def __import_gitlab(import_args, repo_settings):

        import_count = 0

        try:
            client = gitlab.Gitlab(import_args.gitlab_url, private_token=import_args.gitlab_token)

            search = import_args.gitlab_search

            if search:
                search = search.upper()

            prefix = ""
            as_subrepos = False

            if import_args.gitlab_as_depends:
                prefix = import_args.gitlab_depends_prefix
            elif import_args.gitlab_as_subrepos:
                as_subrepos = True
                prefix = import_args.gitlab_subrepos_prefix

            items = client.projects.list(as_list=False, owned=True, order_by="path",
                                         membership=import_args.gitlab_include_membership)

            repositories = {}

            for item in items:
                repositories[item.path_with_namespace] = item

            repositories = collections.OrderedDict(sorted(repositories.items()))

            for path, item in repositories.items():

                src_key = item.name.upper().replace(" ", "")
                folder = os.path.join(prefix, item.name)
                url = item.http_url_to_repo

                if not search or (search and (search in src_key or search in url.upper())):

                    repo_settings.sources.add(src_key=src_key, protocol="GIT", url=url, replace=import_args.force)

                    import_count += 1

                    if not import_args.gitlab_sources_only:
                        Console.print("Importing repo " + src_key + " = " + url + " to " + folder)

                        if as_subrepos:
                            repo_settings.subrepos.add(folder, src_key=src_key, replace=import_args.force)
                        else:
                            repo_settings.dependencies.add(folder, src_key=src_key, replace=import_args.force)
                    else:
                        Console.print("Importing source " + src_key + " = " + url)

        except Exception as e:
            Console.error("Could not retrieve projects from Gitlab: " + str(e))

        return import_count
