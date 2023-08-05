from .client import ImagineClient
from .utils import normalizeMetaHeaders
import pytest

def test_ImagineClient_should_be_created_with_required_props():
    pytest.shared = {
        'client': ImagineClient({
            'apiKey': 'test',
            'clientId': 'test'
        }),
        'validInfer': {}
    }


def test_ImagineClient_should_throw_error_if_missing_apiKey_or_clientId():
    with pytest.raises(Exception):
        badClient = ImagineClient()


def test_ImagineClient_should_get_supported_image_model():
    pytest.shared['client'].getImageModel('phenomenal-face')


def test_ImagineClient_should_throw_an_error_for_invalid_image_model():
    with pytest.raises(Exception):
        pytest.shared['client'].getImageModel('not-so-phenomenal-face')


def test_Utilities_normalizeMetaHeaders():
    expectedResult = {
        'x-imagine-meta-foo': 'foo',
        'x-imagine-meta-bar': 'bar',
        'x-imagine-meta-dog': 42,
        'x-imagine-meta-cat': 'cat',
        'x-imagine-meta-caps': 'AHHHHH',
    }

    normalizedMetaHeaders = normalizeMetaHeaders({
        'foo': 'foo',
        'bar': 'bar',
        'x-imagine-meta-dog': 42,
        'x-imagine-meta-cat': 'cat',
        'X-IMAGINE-META-CAPS': 'AHHHHH'
    })

    assert(expectedResult == normalizedMetaHeaders)


models = [{
    'modelId': 'happy-face',
    'modelName': 'Happy Face',
    'modelType': 'image',
    'validInfer': {
        'resultType': 'selfie',
    },
    'validCorrectedData': {
        'upset': 0,
        'calm': 0,
        'happy': 1.0,
        'sad': 0,
        'surprised': 0,
        'unknown': 0
    },
}, {
    'modelId': 'phenomenal-face',
    'modelName': 'Phenomenal Face',
    'modelType': 'image',
    'validInfer': {
        'resultType': 'selfie',
    },
    'validCorrectedData': {
        'height': 159,
        'weight': 65,
        'age': 36,
        'gender': 'male'
    },
}]

@pytest.mark.parametrize("modelConfig", models)
def test_Models_infer_succeeds_with_valid_image(modelConfig):
    with open('test-face.jpg', 'rb') as file:
        modelId = modelConfig['modelId']

        model = pytest.shared['client'].getImageModel(modelId)
        data = model.infer(file, "false", { 'context': 'test' })
        
        assert(data['type'] == modelConfig['validInfer']['resultType'])

        pytest.shared['validInfer'][modelId] = data

@pytest.mark.parametrize("modelConfig", models)
def test_Models_label_correction_succeeds_with_valid_correction(modelConfig):
    modelId = modelConfig['modelId']
    correctedData = modelConfig['validCorrectedData']

    model = pytest.shared['client'].getImageModel(modelId)
    validInfer = pytest.shared['validInfer'][modelId].copy()
    validInfer.update({
        'data': correctedData
    });
    data = model.correctionLabel(validInfer, { 'context': 'test' })

    assert(data == correctedData)

@pytest.mark.parametrize("modelConfig", models)
def test_Models_label_prediction_succeeds_with_valid_prediction(modelConfig):
    modelId = modelConfig['modelId']
    correctedData = modelConfig['validCorrectedData']

    model = pytest.shared['client'].getImageModel(modelId)
    validInfer = pytest.shared['validInfer'][modelId]
    data = model.predictionLabel(validInfer, { 'context': 'test' })

    assert(data == validInfer['data'])