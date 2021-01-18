# Image Comparison API

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Working within a virtual environment is recommended whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies
Once you have your virtual environment running. Install dependencies by
```bash
pip install -r requirements.txt
```

##### Key Dependencies

- [HTTP servers](https://docs.python.org/3/library/http.server.html) This module defines classes for implementing HTTP servers (Web servers).

- [imgcompare](https://github.com/datenhahn/imgcompare) Calculates the difference between images in percent, checks equality with optional fuzzyness.

- [PIL](https://pillow.readthedocs.io/en/stable/reference/Image.html) The Image module provides a class with the same name which is used to represent a PIL image. The module also provides a number of factory functions, including functions to load images from files, and to create new images.

## Running the server

Ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
python3 server.py
```

## Tasks

## Endpoints Reference

GET '/image-comparison?img_a=<img_path>&img_b=<img_path>&token=<key>'
- Fetches two pictures for comparison
- Fetches one basic token for authentication. For testing purpose current key is 'kmrhn74zgzcq4nqb'
- image_path could be local file or url
- Request Arguments: None
- Returns: A simliarity percentage
- Sample: 
```bash
success : True
percent : 50.0%
```

## Error handling

The error will be return as Text format as followed:
Not found error (404)
```bash
success : False
error : 404
message : resource not found
```

Authentication error (401)
```bash
success : False
error : 401
message : Authetication failed.
```

Authentication error (403)
```bash
success : False
error : 403
message : Invalid credentials
```

## Test
By running the server in the terminal we will be able to run the unit test.
Run the server first by
```bash
python3 server.py
```
Run the test by
```bash
python3 test.py
```

## Authors
Chia-Ning (Jeffrey) Lee is in charged of backend Web Api.
