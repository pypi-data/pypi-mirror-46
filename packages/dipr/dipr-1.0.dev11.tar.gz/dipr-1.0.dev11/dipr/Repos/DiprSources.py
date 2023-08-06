
import os

from ruamel.yaml import YAML

from Utilities.Console import Console
from Repos.DiprSource import DiprSource
from Repos.YamlFile import YamlFile


class DiprSources(YamlFile):

    PROTOCOL_FIELD = "PROTOCOL"
    URL_FIELD = "URL"

    def __init__(self, dipr_source_file):
        super().__init__(dipr_source_file)

    def _parse_item(self, key, values):
        return DiprSource(key, values)

    # def _store_item(self, key, dict_values, stored_values):
    #     for key,value in dict_values:
    #         stored_values[key] = value

    def add(self, src_key, values=None, protocol=None, url=None, replace=False):
        super()._add(src_key, DiprSource(src_key, values=values, protocol=protocol, url=url), replace)


