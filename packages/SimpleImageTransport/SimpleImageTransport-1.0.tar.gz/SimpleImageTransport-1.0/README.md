# SimpleImageTransport

Simple python 3 library for transporting images to a remote machine, applying transformations and returning a response.

## Usage

Start a server on the remote machine:

```python
from SimpleImageTransport import ImageReceiver

# Callback takes a single parameter image and returns a dict of useful data
def example_callback(img):
    return {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}

# Initialize the application
image_receiver = ImageReceiver()
image_receiver.set_callback(example_callback)
image_receiver.run()
```

On the local machine you can send an image and get an appropriate response:

```python
from SimpleImageTransport import ImageSender
import numpy as np

img = np.zeros((1080, 1920))

response = ImageSender(img)
print(response)  # {'message': 'image received. size=1920x1080'}
```