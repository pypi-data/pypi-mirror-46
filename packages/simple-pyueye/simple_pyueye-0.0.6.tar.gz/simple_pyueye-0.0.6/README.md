## Description
This package is a high-level wrapper for the python bindings wrapper [pyueye](https://pypi.org/project/pyueye/).
The package was designed for easier implementation.

### QuickStart
```
$ from simple_pyueye import CameraObj as Camera
$ camera=Camera(CamID)
$ camera.open()
$ camera.capture_still(save=True,filename='img.png')
$ camera.close()
```

### Installation

```sh
$ pip install simple-pyueye
$ pip uninstall enum34  # if your python version is 3.6 or higher
```

### Requirements

Dillinger is currently extended with the following plugins. Instructions on how to use them in your own application are linked below.

| Package | Explanation |
| ------ | ------ |
| pyueye | Python bindings to ueye.dll |
| numpy | array management |
| pywin32 | Capturing Windows events |
| opencv | for the demos live simple pre-processing example |
| pillow | handling images |