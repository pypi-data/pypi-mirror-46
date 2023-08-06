from girder import plugin


class GirderPlugin(plugin.GirderPlugin):
    DISPLAY_NAME = 'metadata_links'
    CLIENT_SOURCE_PATH = 'web_client'

    def load(self, info):
        pass
