"""TBW."""
from pathlib import Path

import click

import tornado.ioloop
import tornado.web
import tornado.websocket

from tornado_image_streamer import camera_utils
from tornado_image_streamer import image_stream_handler


@click.command()
@click.option('-p', '--port', default=8888,
              help='IP port used for the web server (default: 8888)')
@click.option('-s', '--simulate', is_flag=True,
              help='Enable simulated camera.')
@click.option('-m', '--mode',  default='push',
              type=click.Choice(['get', 'push']),
              help='The mode of operation (default: push).')
def main(port=8888, simulate=False, mode='push'):
    """Tornado web server that streams webcam images over the network."""
    pkg_dir = Path(__file__).absolute().parent

    if simulate:
        cam = camera_utils.SimCam()
    else:
        cam = camera_utils.WebCam()

    if mode == 'push':
        streamer_class = image_stream_handler.ImagePushStreamHandler
    else:
        streamer_class = image_stream_handler.ImageStreamHandler

    app = tornado.web.Application(
        handlers=[
            (r"/imagestream", streamer_class),
            (r"/(.*)", image_stream_handler.IndexPageHandler, {
                "path": pkg_dir.joinpath('templates'),
                "default_filename": "index.html",
            }),
        ],
        static_path=pkg_dir.joinpath('static'),
        debug=True,
        camera=cam,
        sockets=[],
        stream_mode=mode,
    )

    if mode == 'push':
        streamer_class.start_read_image_loop(application=app)

    app.listen(port)
    print('http://localhost:8888')
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
