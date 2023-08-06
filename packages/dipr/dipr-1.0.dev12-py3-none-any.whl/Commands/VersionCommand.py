from Utilities.Console import Console
from Utilities.Version import get_version_string, DIPR_URL

from Protocols.ProtocolHelper import get_protocol_status

from Commands.DiprCommandBase import DiprCommandBase


class VersionCommand(DiprCommandBase):

    def __init__(self, user_settings):
        super().__init__(user_settings)

    def execute(self, arguments):
        Console.print(get_version_string())
        Console.print("URL: " + DIPR_URL)
        Console.print()

        Console.print("Supported Protocols:")

        for p in get_protocol_status():
            Console.print(p)
