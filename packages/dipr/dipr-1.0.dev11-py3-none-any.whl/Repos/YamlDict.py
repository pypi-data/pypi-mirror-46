
from ruamel.yaml.comments import CommentedMap


class YamlDict(CommentedMap):

    def __init__(self, key, values=None):
        super().__init__()

        self.__yaml_root_key = str(key).strip()

        if values:
            self._add_values(values)

    @property
    def yaml_root_key(self):
        return self.__yaml_root_key

    def _add_values(self, values):
        if not values:
            return

        for key, value in values.items():
            self[key.upper()] = value

    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)
        else:
            return None
