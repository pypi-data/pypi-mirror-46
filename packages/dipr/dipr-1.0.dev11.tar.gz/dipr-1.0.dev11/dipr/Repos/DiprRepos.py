import os
from ruamel.yaml import YAML

from Utilities.Console import Console
from Repos.DiprRepo import DipRepo
from Repos.YamlFile import YamlFile


class DiprRepos(YamlFile):

    def __init__(self, dipr_repo_file):
        super(DiprRepos, self).__init__(dipr_repo_file)

    def _parse_item(self, repo_path, values):
        return DipRepo(repo_path, values=values)

    # def _store_item(self, key, dict_values, stored_values):
    #     stored_values[DipRepos.SRC_KEY_KEY] = dict_values.key
    #
    #     if dict_values.revision:
    #         stored_values[DipRepos.REVISION_KEY] = dict_values.revision
    #     elif dict_values.tag:
    #         stored_values[DipRepos.TAG_KEY] = dict_values.tag
    #     elif dict_values.branch:
    #         stored_values[DipRepos.BRANCH_KEY] = dict_values.branch

    def add(self, repo_path, values=None, src_key=None, revision=None, tag=None, branch=None, replace=False):
        dr = DipRepo(repo_path, values=values, src_key=src_key, revision=revision, tag=tag, branch=branch)
        super()._add(dr.repo_key, dr, replace=replace)

    def remove_repo(self, repo):
        self.remove(repo.repo_key)

    def get_entries_for_key(self, key):
        entries = []

        key = key.upper()

        for p, v in self.items():
            if v.src_key.upper() == key:
                entries.append(v)

        return entries

