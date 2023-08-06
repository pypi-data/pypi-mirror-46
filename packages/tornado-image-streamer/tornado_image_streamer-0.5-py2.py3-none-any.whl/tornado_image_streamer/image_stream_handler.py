"""TBW."""
# import typing as t
import threading
import time
import asyncio
import logging

import tornado.ioloop
import tornado.web
import tornado.websocket


logger = logging.getLogger(__name__)


class IndexPageHandler(tornado.web.RequestHandler):
    """The index.html HTML generation handler."""

    def __init__(self, application, request, **kwargs):
        """TBW."""
        self._path = kwargs.pop("path")
        self.default_filename = kwargs.pop("default_filename", "index.html")
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

    def on_connection_close(self):
        """TBW."""
        self.close()

    @staticmethod
    def start(application):
        """TBW."""
        pass  # unused, for API compatibility with ImagePushStreamHandler

    @staticmethod
    def stop():
        """TBW."""
        pass  # unused, for API compatibility with ImagePushStreamHandler

    async def on_message(self, message):
        """TBW."""
        self.counter += 1
        try:
            if message == '?':
                image = self.application.settings['camera'].read_image()
                await self.write_message(image, binary=True)
            else:
                await self.write_message(message)  # echo
        except Exception as exc:
            logger.exception(exc)


class ImagePushStreamHandler(tornado.websocket.WebSocketHandler):
    """TBW."""

    # images = []  # type: t.List[ImagePushStreamHandler]
    interval = 1
    stop_event = threading.Event()

    def __init__(self, *args, **kwargs):
        """TBW."""
        super().__init__(*args, **kwargs)
        self.counter = 0
        self.images = []
        self._periodic = tornado.ioloop.PeriodicCallback(self._write_queue, 40)
        self._periodic.start()
        self.application.settings['sockets'].append(self)

    def on_connection_close(self):
        """TBW."""
        logger.info('Closing web socket...')
        self.close()
        self._periodic.stop()
        try:
            self.application.settings['sockets'].remove(self)
        except ValueError:
            pass

    @staticmethod
    def start(application):
        """TBW."""
        th = threading.Thread(target=ImagePushStreamHandler.read_image_loop,
                              args=(application,),
                              name='read-camera')
        th.start()

    @staticmethod
    def stop():
        """TBW."""
        ImagePushStreamHandler.stop_event.set()

    @staticmethod
    def read_image_loop(application):
        """TBW."""
        cam = application.settings['camera']
        while not ImagePushStreamHandler.stop_event.is_set():
            interval = float(ImagePushStreamHandler.interval) / 1000.0
            if interval > 0:
                if len(application.settings['sockets']):
                    image = cam.read_image()
                    for ws in application.settings['sockets']:
                        ws.images.append(image)
                interval = 0.001
            else:
                interval = 1.0  # paused
            time.sleep(interval)
        logger.info('Exiting ImagePushStreamHandler.read_image_loop')

    async def _write_queue(self):
        """TBW."""
        for _ in range(50):
            if self.images:
                break
            await asyncio.sleep(0.001)

        while self.images:
            image = self.images.pop()
            self.images.clear()
            try:
                await self.write_message(image, binary=True)
            except tornado.websocket.WebSocketClosedError:
                self.close()
                socks = self.application.settings['sockets']
                if self in socks:
                    socks.remove(self)

    async def on_message(self, message):
        """TBW."""
        self.counter += 1
        try:
            if message == '?':
                await self._write_queue()
            elif message.startswith('interval'):
                interval = int(message.split('=')[-1])
                self._periodic = interval
                ImagePushStreamHandler.interval = interval
                # self.write_message(message)  # echo
        except Exception as exc:
            logger.exception(exc)
