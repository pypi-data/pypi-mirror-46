from .image_based_model import ImageBasedModel

SupportedImageBasedModels = [
    'phenomenal-face',
    'happy-face'
]

def getImageModel(client, modelId):
    if modelId in SupportedImageBasedModels:
        return ImageBasedModel(client, modelId)
    raise Exception(
        'Image Model [{0}] is not supported.\r\n Supported image models: {1}'.format(
            modelId,
            SupportedImageBasedModels
        )
    )
