
from Utilities.Console import Console

from Commands.DiprCommandBase import DiprCommandBase

from Protocols.ProtocolHelper import resolve_repo_handler


class InitCommand(DiprCommandBase):

    def __init__(self, user_settings):
        super().__init__(user_settings)

    def execute(self, arguments):
        repo_settings = super()._open_repo(arguments)

        if repo_settings.is_initialized:
            Console.warning("Repo '" + str(repo_settings.root_repo_path) + "' is already initialized.")

            if arguments.init_command.force:
                Console.warning("Force flag was set, reinitializing...")
            else:
                return
        else:
            Console.print("Initializing repo '" + str(repo_settings.root_repo_path) + "'...")

        repo_settings.initialize(arguments.init_command.force)

        if arguments.init_command.no_add:
            return

        handler = resolve_repo_handler(full_repo_path=repo_settings.root_repo_path)

        if handler is None:
            Console.warning("The root repo '" + str(repo_settings.root_repo_path) +
                            "' is not a recognized revision control system.  "
                            "Initialized files are not added to revision control.")
        else:
            InitCommand.__add_file(handler, repo_settings.dipr_src_file_path)
            InitCommand.__add_file(handler, repo_settings.dipr_dep_file_path)
            InitCommand.__add_file(handler, repo_settings.dipr_sub_file_path)

        Console.print("Complete.")

    @staticmethod
    def __add_file(repo, file):
        if not repo.is_tracked(file):
            repo.add(file)
