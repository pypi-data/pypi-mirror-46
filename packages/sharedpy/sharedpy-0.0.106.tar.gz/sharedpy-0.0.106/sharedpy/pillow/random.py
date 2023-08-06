from io import BytesIO

import requests
from PIL import Image




def get_random_image():
    '''
    Returns a Pillow instance populated randomly from the splashbase.co API, as well as the image's URL
    Images from splashbase.co frequently have populated EXIF data (good for testing)
    '''
    r = requests.get('http://www.splashbase.co/api/v1/images/random?images_only=true');
    url = r.json().get('url', None)
    with requests.get(url, stream=True) as r:
        r = requests.get(url)
        return url, Image.open(BytesIO(r.content))
