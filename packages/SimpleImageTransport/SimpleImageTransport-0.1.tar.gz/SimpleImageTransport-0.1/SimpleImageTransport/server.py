import json

import cv2
import requests
import numpy as np


def send_image(image: np.array, host: str = "0.0.0.0", port: int = 5000, endpoint: str = "/api/image") -> dict:
    """Utility function to send numpy image to api endpoint

    :param image: Image in the format of a uint8 numpy array
    :param host: Remote IP address
    :param port: Remote address port
    :param endpoint: The api endpoint set in the image receiver
    :return: Response dictionary containing endpoint response
    """
    headers = {'content-type': 'image/jpeg'}
    post_url = "http://{}:{}{}".format(host, port, endpoint)
    _, img_encoded = cv2.imencode('.jpg', image)
    post_response = requests.post(post_url, data=img_encoded.tostring(), headers=headers)
    return json.loads(post_response.text)


if __name__ == '__main__':
    while True:
        img = cv2.imread('test.png')
        response = send_image(img)
        print(response)
