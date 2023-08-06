
from Errors.DiprError import DiprError


class SettingsError(DiprError):

    def __init__(self, message):
        self.message = message
