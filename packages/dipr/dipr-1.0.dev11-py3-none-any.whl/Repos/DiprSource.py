
from Repos.YamlDict import YamlDict


class DiprSource(YamlDict):

    PROTOCOL_FIELD = "PROTOCOL"
    URL_FIELD = "URL"

    def __init__(self, src_key, values=None, protocol=None, url=None):
        super().__init__(src_key, values=values)

        if protocol:
            self[DiprSource.PROTOCOL_FIELD] = protocol

        if url:
            self[DiprSource.URL_FIELD] = url

    @property
    def src_key(self):
        return super().yaml_root_key

    @property
    def protocol(self):
        return self[DiprSource.PROTOCOL_FIELD]

    @property
    def url(self):
        return self[DiprSource.URL_FIELD]

    def __str__(self):
        return self.src_key + ' = ' + self.protocol + ', ' + self.url
