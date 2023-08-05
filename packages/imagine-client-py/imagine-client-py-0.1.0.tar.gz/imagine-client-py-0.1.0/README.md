# Imagine Client for Python

This library allows you to easily connect to doc.ai's Imagine API.

## Supported Image Models

Model Id       | Type  | Description |
---------------|-------|-------------|
phenomenal-face| image | Given a facial image, this model infers the age, sex, height and weight of a person |
happy-face     | image | Given a facial image, this model infers the mood of a person | 


## API

```client.getImageModel(modelId)```

> Given a string (modelId), gets the image model. See the *"Supported Image Models"* section for a list of supported model ids

```imageModel.infer(imageFileStream, shouldStoreImage, metadata)```

> Performs the model's inference on an image. A read stream should be passed as the parameter (imageFileStream).

```imageModel.correctionLabel(correctionDict, metadata)```

> Uploads a correction label to the imagine API, for a given inference.

```imageModel.predictionLabel(predictionDict, metadata)```

> (FOR EDGE PREDICTIONS) Uploads a prediction label to the imagine API, for a given inference.

### Example

```python

from imagine_client_py import client

# Initialize imagine client
imagine = client.ImagineClient({
  apiKey: '1234567890',
  clientId: '3ad839e3-90e7-4564-b3a1-5e39c88545a5'
});

# Get a reference to the 'happy-face' model
model = imagine.getImageModel('happy-face');

# Create a read stream to a image file
with open('test-face.jpg', 'rb') as imageFaceFile:
  # Perform the model's inference, on the image.
  result = model.infer(imageFaceFile, "false")

  # Print the result
  print(result);
```