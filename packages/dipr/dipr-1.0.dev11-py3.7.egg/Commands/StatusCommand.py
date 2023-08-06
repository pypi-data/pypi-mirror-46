from Utilities.Console import Console

from Commands.DiprCommandBase import DiprCommandBase


class StatusCommand(DiprCommandBase):

    def __init__(self, user_settings):
        super().__init__(user_settings)

    def execute(self, arguments):
        repo_settings = super()._open_repo(arguments)

        if not repo_settings.is_initialized:
            Console.error("Repo " + str(repo_settings.root_repo_path) + " is not initialized.")
            return

        status_arguments = arguments.status_command

        repo_handler = repo_settings.root_repo_handler

        Console.print("### Root path " + str(repo_settings.root_repo_path) + " ###")

        if repo_handler:
            if repo_handler.has_changes():
                Console.print("[#] The base repo has uncommitted changes.")
            elif repo_handler.is_empty():
                Console.print("[X] The base repo is empty (no change sets).")
            else:
                Console.print("[ ] The base repo is clean.")
        else:
            Console.print("[X] The base directory is not a supported revision control system.")

        Console.print()

        if status_arguments.all or status_arguments.depends_only:
            StatusCommand.__display_depends_status(repo_settings)

        if status_arguments.all or status_arguments.subrepos_only:
            StatusCommand.__display_subrepos_status(repo_settings)

    @staticmethod
    def __display_depends_status(repo_settings):
        StatusCommand.__display_repo_status("Dependencies", repo_settings.resolved_dependencies)

    @staticmethod
    def __display_subrepos_status(repo_settings):
        StatusCommand.__display_repo_status("Sub-Repositories", repo_settings.resolved_subrepos)

    @staticmethod
    def __display_repo_status(repo_type, resolved_repo_list):
        Console.print("### " + repo_type + " (" + str(len(resolved_repo_list)) + ") ###")

        for rr in resolved_repo_list:
            if not rr.handler:
                continue

            Console.print(str(rr.status))

        Console.print()


