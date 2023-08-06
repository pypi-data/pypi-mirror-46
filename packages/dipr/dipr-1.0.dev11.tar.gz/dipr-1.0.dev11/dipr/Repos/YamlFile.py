
import os

from ruamel.yaml import YAML
from ruamel.yaml.parser import ParserError
from Utilities.Console import Console


class YamlFile(dict):

    KEY_IGNORE_PREFIX = "__"

    def __init__(self, yaml_file):
        super(YamlFile, self).__init__()
        self.yaml_file = yaml_file
        self.removal_list = []

    def _add(self, key, value, replace=False):
        if key in self and not replace:
            Console.warning("Key " + key + " already exists.  Ignoring new entry.")
            return

        self[key] = value

    def _parse_item(self, key, values):
        raise NotImplementedError

    def _store_item(self, key, dict_values, stored_values):
        for value_key,value in dict_values.items():
            stored_values[value_key] = value

    def remove(self, key):
        if key in self:
            self.pop(key, None)
            self.removal_list.append(key)

    def load(self):
        if not os.path.isfile(self.yaml_file):
            return

        with open(self.yaml_file, 'r') as file:
            yaml=YAML()
            yaml.allow_duplicate_keys = True

            try:
                entries = yaml.load(file)
            except ParserError as e:
                Console.warning("A parser error was encountered in " + str(self.yaml_file) + ". No entries loaded.")
                return

            if entries is None:
                return

            for key, values in entries.items():
                if key is None or key.startswith(YamlFile.KEY_IGNORE_PREFIX):
                    continue

                try:
                    item = self._parse_item(key, values)

                    orig_key = key
                    key = item.yaml_root_key

                    if key != orig_key:
                        Console.warning("Fixing key format for: " + orig_key + " to " + key)
                        self.removal_list.append(orig_key)

                    if key in self:
                        Console.warning("Duplicate key detected: " + key + ".  Entry will be overridden.")

                    self[key] = item
                except Exception as e:
                    Console.warning("Could not parse values for key: " + key + ". Entry ignored.")
                    Console.info("Exception: " + str(e))

    def save(self):
        entries = None

        with open(self.yaml_file, 'r') as file:
            yaml=YAML()
            yaml.allow_duplicate_keys = True
            entries = yaml.load(file)

        if entries is None:
            entries = dict()

        for key, dict_values in self.items():
            stored_values = dict()
            self._store_item(key, dict_values, stored_values)
            entries[key] = stored_values

        for key in self.removal_list:
            if key in entries:
                entries.pop(key, None)

        if "__END" in entries:
            entries.pop("__END")
            entries.insert(len(entries), "__END", None, "Comment Preservation")

        with open(self.yaml_file, 'w') as file:
            yaml = YAML()
            yaml.dump(entries, file)

