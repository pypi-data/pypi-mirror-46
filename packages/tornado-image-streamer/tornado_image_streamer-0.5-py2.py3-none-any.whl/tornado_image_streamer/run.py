"""TBW."""
from pathlib import Path
import click

import tornado.ioloop
import tornado.web
import tornado.websocket

from tornado_image_streamer import camera_utils
from tornado_image_streamer import image_stream_handler
from tornado_image_streamer import tornado_utils
from tornado_image_streamer import __version__


@click.command()
@click.option('-p', '--port', default=0,
              help='IP port used for the web server (default: 0)')
@click.option('-s', '--simulate', is_flag=True,
              help='Enable simulated camera.')
@click.option('-m', '--mode',  default='push',
              type=click.Choice(['get', 'push']),
              help='The mode of operation (default: push).')
@click.option('-v', '--verbosity', count=True, help='The verbosity level.')
@click.version_option(version=__version__)
def main(port=8888, simulate=False, mode='push', verbosity=0):
    """Tornado web server that streams webcam images over the network."""
    tornado_utils.config_logging(verbosity)

    pkg_dir = Path(__file__).absolute().parent

    camera_class = [
        camera_utils.WebCam,
        camera_utils.SimCam
    ][simulate]

    streamer_class = {
        'push': image_stream_handler.ImagePushStreamHandler,
        'get': image_stream_handler.ImageStreamHandler,
    }[mode]

    app = tornado.web.Application(
        handlers=[
            (r"/imagestream", streamer_class),
            (r"/(.*)", image_stream_handler.IndexPageHandler, {
                "path": pkg_dir.joinpath('templates'),
                "default_filename": "index.html",
            }),
        ],
        template_path=pkg_dir.joinpath('templates'),
        static_path=pkg_dir.joinpath('static'),
        debug=True,
        camera=camera_class(),
        sockets=[],
        timers=[],
        stream_mode=mode,
    )

    streamer_class.start(application=app)
    server = app.listen(port)
    tornado_utils.log_url(server)
    try:
        tornado.ioloop.IOLoop.current().start()
    finally:
        streamer_class.stop()
        tornado_utils.stop_application(app.settings['sockets'])


if __name__ == "__main__":
    main()
