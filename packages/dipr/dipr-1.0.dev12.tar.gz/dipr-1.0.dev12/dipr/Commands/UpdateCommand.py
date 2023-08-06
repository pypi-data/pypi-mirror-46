from Utilities.Console import Console

from Commands.DiprCommandBase import DiprCommandBase
from Protocols.ProtocolHelper import resolve_repo_handler


class UpdateCommand(DiprCommandBase):

    def __init__(self, user_settings):
        super().__init__(user_settings)

    def execute(self, arguments):
        update_args = arguments.update_command

        repo_settings = super()._open_repo(arguments)

        if not repo_settings.is_initialized:
            Console.error("Repo " + repo_settings.root_repo_path + " is not initalized.")
            return

        if update_args.reset:
            Console.print("Reset has been specified.  Changes could be permanently lost.  Continue?")
            answer = input("[y/N]: ").upper()

            if not (answer == "Y" or answer == "YES"):
                return

        if update_args.depends_only or update_args.all_repos:
            UpdateCommand.__execute_on_repo(repo_settings.resolved_dependencies, update_args)

        if update_args.subrepos_only or update_args.all_repos:
            UpdateCommand.__execute_on_repo(repo_settings.resolved_subrepos, update_args)

    @staticmethod
    def __execute_on_repo(all_repos, arguments):
        for repo in all_repos:
            handler = repo.handler

            if handler is None:
                Console.warning("Could not resolve " + repo.src_key + " to a protocol.  Skipping.")
                continue

            UpdateCommand.update_repo(repo, arguments.reset)

            # Console.print("Updating " + str(repo))
            # Console.push_indent()
            #
            # if handler.is_empty():
            #     Console.warning("Repo has no revisions and will not be updated.")
            # else:
            #     handler.update(arguments.reset)
            #
            # Console.print(str(repo.status))
            #
            # Console.print("Complete")
            # Console.pop_indent()

    @staticmethod
    def update_repo(repo, reset=False):
        Console.print("Updating " + str(repo))
        Console.push_indent()

        handler = repo.handler

        if handler.is_empty():
            Console.warning("Repo has no revisions and will not be updated.")
        else:
            handler.update(reset)

        Console.print(str(repo.status))

        Console.print("Complete")
        Console.pop_indent()
