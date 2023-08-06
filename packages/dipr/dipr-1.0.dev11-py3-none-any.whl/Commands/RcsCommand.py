from Utilities.Console import Console

from Commands.DiprCommandBase import DiprCommandBase


class RcsCommand(DiprCommandBase):

    def __init__(self, user_settings):
        super().__init__(user_settings)

    def execute(self, arguments):
        repo_settings = super()._open_repo(arguments)

        rcs_arguments = arguments.rcs_command

        command = rcs_arguments.command.lower()

        if command == "commit":
            RcsCommand._commit(repo_settings, rcs_arguments)
        elif command == "tag":
            RcsCommand._tag(repo_settings, rcs_arguments)
        elif command == "push":
            RcsCommand._push(repo_settings, rcs_arguments)
        elif command == "discard":
            RcsCommand._discard(repo_settings, rcs_arguments)

    @staticmethod
    def _commit(repo_settings, arguments):
        if repo_settings.root_repo_handler and not arguments.exclude_root and repo_settings.root_repo_handler.has_changes():
            Console.print("Committing root repo " + str(repo_settings.root_repo_path) + "...")
            repo_settings.root_repo_handler.commit(arguments.message, arguments.add_remove)

        if not arguments.exclude_subrepos:
            for r in repo_settings.resolved_subrepos:
                if not r.handler:
                    continue

                if r.handler.has_changes():
                    Console.print("Committing: " + str(r.repo_path) + "...")
                    Console.push_indent()
                    r.handler.commit(arguments.message, arguments.add_remove)
                    Console.pop_indent()
                else:
                    Console.print("No changes in " + str(r.repo_path))

    @staticmethod
    def _tag(repo_settings, arguments):
        if not arguments.tag_name:
            Console.error("The tag name cannot be blank.")
            return

        if repo_settings.root_repo_handler and not arguments.exclude_root:
            Console.print("Tagging root repo: " + arguments.tag_name + "...")
            repo_settings.root_repo_handler.tag(arguments.tag_name, arguments.message)

        if not arguments.exclude_subrepos:
            for r in repo_settings.resolved_subrepos:
                if not r.handler:
                    continue

                Console.print("Tagging " + str(r.repo_path) + ": " + arguments.tag_name + "...")
                Console.push_indent()
                r.handler.tag(arguments.tag_name, arguments.message)
                Console.pop_indent()

    @staticmethod
    def _push(repo_settings, arguments):
        if repo_settings.root_repo_handler and not arguments.exclude_root:
            Console.print("Pushing changes in root repo...")
            repo_settings.root_repo_handler.push(arguments.force)

        if not arguments.exclude_subrepos:
            for r in repo_settings.resolved_subrepos:
                if not r.handler:
                    continue

                Console.print("Pushing changes in " + str(r.repo_path) + "...")
                Console.push_indent()
                r.handler.push(arguments.force)
                Console.pop_indent()

    @staticmethod
    def _discard(repo_settings, arguments):
        Console.print("This will permanently remove modified and untracked files.  Continue?")
        answer = input("[y/N]: ").upper()

        if not (answer == "Y" or answer == "YES"):
            return

        if repo_settings.root_repo_handler and not arguments.exclude_root:
            if repo_settings.root_repo_handler.has_changes():
                Console.print("Discarding changes in root repo...")
                repo_settings.root_repo_handler.discard()
            else:
                Console.print("The root repo has no changes.")

        if arguments.include_depends:
            Console.print("### Discarding changes in dependencies... ###")
            for r in repo_settings.resolved_dependencies:
                if not r.handler:
                    continue

                if r.handler.has_changes():
                    Console.print("Discarding changes in " + str(r.repo_path) + "...")
                    Console.push_indent()
                    r.handler.discard()
                    Console.pop_indent()
                else:
                    Console.print("There are no changes in " + str(r.repo_path))

                Console.print()

        if not arguments.exclude_subrepos:
            Console.print("### Discarding changes in sub-repositories... ###")
            for r in repo_settings.resolved_subrepos:
                if not r.handler:
                    continue

                if r.handler.has_changes():
                    Console.print("Discarding changes in " + str(r.repo_path) + "...")
                    Console.push_indent()
                    r.handler.discard()
                    Console.pop_indent()
                else:
                    Console.print("There are no changes in " + str(r.repo_path))
