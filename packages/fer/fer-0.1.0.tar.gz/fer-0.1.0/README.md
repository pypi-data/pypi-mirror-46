FER
===

Facial expression recognition.

![image](https://github.com/justinshenk/fer/raw/master/result.jpg)

[![PyPI version](https://badge.fury.io/py/fer.svg)](https://badge.fury.io/py/fer) [![Build Status](https://travis-ci.org/justinshenk/fer.svg?branch=master)](https://travis-ci.org/justinshenk/fer)

INSTALLATION
============

Currently FER only supports Python3.4 onwards. It can be installed
through pip:

```bash
$ pip3 install fer
```

This implementation requires OpenCV\>=3.2 and Tensorflow\>=1.7.0
installed in the system, with bindings for Python3.

They can be installed through pip (if pip version \>= 9.0.1):

```bash
$ pip3 install tensorflow>=1.7 opencv-contrib-python==3.3.0.9
```

or compiled directly from sources
([OpenCV3](https://github.com/opencv/opencv/archive/3.4.0.zip),
[Tensorflow](https://www.tensorflow.org/install/install_sources)).

Note that a tensorflow-gpu version can be used instead if a GPU device
is available on the system, which will speedup the results. It can be
installed with pip:

```bash
$ pip3 install tensorflow-gpu\>=1.7.0
```

USAGE
=====

The following example illustrates the ease of use of this package:

```python
from fer.fer import FER
import cv2

img = cv2.imread("justin.jpg")
detector = FER()
print(detector.detect_emotions(img))
```

Sample output:
```
[{'box': [277, 90, 48, 63], 'emotions': {'angry': 0.02, 'disgust': 0.0, 'fear': 0.05, 'happy': 0.16, 'neutral': 0.09, 'sad': 0.27, 'surprise': 0.41}]
```

For recognizing facial expressions in video, the `Video` class splits video into frames. It can use a local Keras model (default) or Peltarion API for the backend:

```python
from fer.classes import Video

video = Video(video_filename)
# Analyze video, displaying the output
raw_data = video.analyze(detector, display=True)
df = video.to_pandas(raw_data)
```

The detector returns a list of JSON objects. Each JSON object contains
two keys: 'box' and 'emotions':

-   The bounding box is formatted as [x, y, width, height] under the key
    'box'.
-   The emotions are formatted into a JSON object with the keys 'anger',
    'disgust', 'fear', 'happy', 'sad', surprise', and 'neutral'.

Other good examples of usage can be found in the files
[example.py](example.py) and [video-example.py](video-example.py)
located in the root of this repository.

MODEL
=====

FER bundles a Keras model, as well as support for [Peltarion](https://peltarion.com) API.

The model is a convolutional neural network with weights saved to HDF5
file in the `data` folder relative to the module's path. It can be
overriden by injecting it into the `FER()` constructor during
instantiation with the `emotion_model` parameter.

LICENSE
=======

[MIT License](LICENSE).

CREDIT
======

This code includes methods and package structure copied or derived from
Iván de Paz Centeno's [implementation](https://github.com/ipazc/mtcnn/)
of MTCNN and Octavia Arriaga's [facial expression recognition
repo](https://github.com/oarriaga/face_classification/).

REFERENCE
---------
