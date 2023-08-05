import requests
from .utils import normalizeMetaHeaders

class ImageBasedModel:
    def __init__(self, client, modelId):
        self.client = client
        self.modelId = modelId
        self.modelType = 'image'
    
    def _postLabelData(self, data, metatype, metadata = {}):
        url = "{0}/{1}/{2}/label".format(
            self.client.config['baseUrl'],
            self.client.config['apiVersion'],
            self.modelId
        )

        headers = normalizeMetaHeaders(metadata);
        headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-imagine-meta-type': metatype,
        })

        response = requests.post(
            url, 
            json=data,
            headers=headers
        )

        if response.ok:
            return response.json()
        else:
            raise Exception(
                "Error making request to the /label ({0}) endpoint. Status code {1}".format(
                    metatype,
                    response.status_code
                )
            )

    def infer(self, imageFile, shouldSaveImage, metadata = {}):
        url = "{0}/{1}/{2}/infer".format(
            self.client.config['baseUrl'],
            self.client.config['apiVersion'],
            self.modelId
        )

        headers = normalizeMetaHeaders(metadata);
        headers.update({
            'Accept': 'application/json'
        })

        response = requests.post(
            url,
            headers=headers,
            files={
                'image': imageFile,
                'store': shouldSaveImage
            }
        )

        if response.ok:
            return response.json()
        else:
            raise Exception(
                "Error making request to the /infer endpoint. Status code {0}".format(
                    response.status_code
                )
            )
    
    def correctionLabel(self, correctionsDict, metadata):
        return self._postLabelData(correctionsDict, 'correction', metadata);

    def predictionLabel(self, correctionsDict, metadata):
        return self._postLabelData(correctionsDict, 'prediction', metadata);
    