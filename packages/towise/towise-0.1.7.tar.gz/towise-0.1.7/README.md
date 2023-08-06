
# TOWISE PYTHON API
Towise assists you to detect human faces and bodies with using the latest and reliable technology.

## Getting Started
### Prerequisites 
```
 Python 3.6.5
 pip 19.1 

```
### Installing
To install the package

```sh
pip install towise 
```
To import your project
```python
from towise import Towise
```
### Using Towise
You must enter appKey and appId

For Example:
```python
from towise import Towise

if __name__ = "__main__":
    image_url = "https://cdn.onebauer.media/one/media/5c6e/80bc/d007/9656/5f0a/6c12/dua-lipa-brits.jpg"
    t = Towise('your appId','your appKey')

    # for face detection
    print(t.faceDetect(image_url))

    # for emotion detection
    print(t.emotionDetect(image_url))

    # for body detection
    print(t.bodyDetect(image_url))

    # for face comparing
    print(t.bodyDetect(image_url))
```

## Versioning
For the versions available, see the https://github.com/argedor/TowiseNodeJSAPI/tags

## Authors
* **Harun Keleşoğlu** - *Developer* - [Github](https://github.com/harunkelesoglu)
See also the list of [contributers](https://github.com/argedor/TowiseNodeJSAPI/graphs/contributors)

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details