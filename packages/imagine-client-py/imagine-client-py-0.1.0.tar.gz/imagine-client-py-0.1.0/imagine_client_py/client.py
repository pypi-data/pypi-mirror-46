from .models import getImageModel

DEFAULT_BASE_URL = 'https://imagine.doc.ai'
DEFAULT_IMAGINE_API_VERSION = 'v0.2.3'

class ImagineClient:
    def __init__(self, config):
        defaultConfig = {
            "baseUrl": DEFAULT_BASE_URL,
            "apiVersion": DEFAULT_IMAGINE_API_VERSION,
            "apiKey": None,
            "clientId": None
        }

        self.config = defaultConfig
        self.config.update(config)

        if self.config['apiKey'] is None:
            raise Exception('You must specify an API Key (apiKey)')

        if self.config['clientId'] is None:
            raise Exception('You must specify a clientId (clientId)')
    
    def getImageModel(self, modelId):
        return getImageModel(self, modelId)