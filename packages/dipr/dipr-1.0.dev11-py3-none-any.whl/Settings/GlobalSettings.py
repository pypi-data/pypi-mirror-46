
from pathlib import Path

from Settings.RepoSettings import RepoSettings


class GlobalSettings(object):

    TEMPLATE_DIRECTORY = "Templates"

    def __init__(self, dipr_path):
        self.dipr_path = Path(dipr_path)
        self.dipr_template_directory = Path(self.dipr_path, GlobalSettings.TEMPLATE_DIRECTORY)
        self.dipr_src_template_file_path = Path(self.dipr_template_directory, RepoSettings.DIPR_SRC_FILE)
        self.dipr_dep_template_file_path = Path(self.dipr_template_directory, RepoSettings.DIPR_DEP_FILE)
        self.dipr_sub_template_file_path = Path(self.dipr_template_directory, RepoSettings.DIPR_SUB_FILE)

