"""TBW."""
import typing as t
import threading
import time

import tornado.ioloop
import tornado.web
import tornado.websocket


class IndexPageHandler(tornado.web.RequestHandler):
    """The index.html HTML generation handler."""

    def __init__(self, application, request, **kwargs):
        """TBW."""
        self._path = kwargs.pop("path")
        self.default_filename = kwargs.pop("default_filename")
        super(IndexPageHandler, self).__init__(application, request, **kwargs)

    def get(self, *args, **kwargs):
        """TBW."""
        self.render(self.default_filename, app=self.application)


class ImageStreamHandler(tornado.websocket.WebSocketHandler):
    """TBW."""

    def __init__(self, *args, **kwargs):
        """TBW."""
        self.counter = 0
        super().__init__(*args, **kwargs)

    def on_message(self, message):
        """TBW."""
        self.counter += 1
        try:
            if message == '?':
                image = self.application.settings['camera'].read_image()
                self.write_message(image, binary=True)
            else:
                self.write_message(message)  # echo
        except Exception as exc:
            print(exc)


class ImagePushStreamHandler(tornado.websocket.WebSocketHandler):
    """TBW."""

    images = []  # type: t.List[ImagePushStreamHandler]
    interval = 1

    def __init__(self, *args, **kwargs):
        """TBW."""
        self.counter = 0
        super().__init__(*args, **kwargs)
        self.application.settings['sockets'].append(self)
        tornado.ioloop.PeriodicCallback(self._write_queue, 1).start()

    @staticmethod
    def start_read_image_loop(application):
        """TBW."""
        th = threading.Thread(target=ImagePushStreamHandler.read_image_loop,
                              args=(application,),
                              name='read-camera')
        th.start()

    @staticmethod
    def read_image_loop(application):
        """TBW."""
        cam = application.settings['camera']
        while True:
            interval = float(ImagePushStreamHandler.interval) / 1000.0
            if interval > 0:
                if len(application.settings['sockets']):
                    image = cam.read_image()
                    ImagePushStreamHandler.images.append(image)
            else:
                interval = 1.0  # paused
            time.sleep(interval)

    def _write_queue(self):
        """TBW."""
        while self.images:
            image = self.images.pop()
            try:
                self.write_message(image, binary=True)
            except tornado.websocket.WebSocketClosedError:
                self.close()
                socks = self.application.settings['sockets']
                if self in socks:
                    socks.remove(self)

    def on_message(self, message):
        """TBW."""
        self.counter += 1
        try:
            if message == '?':
                self._write_queue()
            elif message.startswith('interval'):
                interval = int(message.split('=')[-1])
                ImagePushStreamHandler.interval = interval
                # self.write_message(message)  # echo
        except Exception as exc:
            print(exc)
