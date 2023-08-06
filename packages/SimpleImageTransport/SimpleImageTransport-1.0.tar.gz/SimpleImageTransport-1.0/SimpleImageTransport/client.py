from typing import Callable
from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2


class FlaskImageReceiver:
    def __init__(self, host: str = "0.0.0.0", port: int = 5000, callback: Callable = None, endpoint: str = "/api/image",
                 name: str = __name__) -> None:
        """Provides an easy to use interface to send/receive image information over a network connection

        :param host: IP address to host server/remote service on
        :param port: Port address to host server/remote service on
        :param callback: Function to modify received images and return a dict
        :param endpoint: The api endpoint set in the image receiver
        :param name: Name of the underlying flask application
        """
        self.host = host
        self.port = port
        self.callback = None
        self.endpoint = endpoint

        self.app = Flask(name)
        if callback is not None:
            self.set_callback(callback)
        self.app.route(self.endpoint, methods=['POST'])(self.receive_image)

    def set_callback(self, callback: Callable) -> None:
        """Sets the modification function applied to received images

        :param callback: Function to modify received images and return a dict
        """
        if callable(callback):
            self.callback = callback
        else:
            raise ValueError("Parameter callback is not callable")

    def run(self) -> None:
        """Starts the application and endpoint handlers
        """
        self.app.run(host=self.host, port=self.port)

    def receive_image(self):
        """API endpoint function to process received images

        :return: Dict of endpoint response/callback return
        """
        # Convert string of image data to uint8
        img_encoded = np.frombuffer(request.data, np.uint8)

        # Decode image
        img = cv2.cvtColor(cv2.imdecode(img_encoded, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)

        response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}

        # Call the function and get response dict
        if self.callback is not None and callable(self.callback):
            callback_response = self.callback(img)
            if isinstance(callback_response, dict):
                response = callback_response

        response_pickled = jsonpickle.encode(response)
        return Response(response=response_pickled, status=200, mimetype="application/json")


if __name__ == '__main__':
    def example_callback(img):
        return {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])}

    # Initialize the Flask application
    flask_receiver = FlaskImageReceiver()
    flask_receiver.set_callback(example_callback)
    flask_receiver.run()

