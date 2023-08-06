"""TBW."""
import typing as t
import threading
import logging
import tornado.ioloop


def config_logging(verbosity: int) -> None:
    """Configure logging facility."""
    levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    logging_level = levels[min(verbosity, len(levels)-1)]
    log_format = '%(asctime)s - %(levelname)s - %(name)s - ' \
                 '%(funcName)s - %(threadName)s - %(message)s'
    logging.basicConfig(level=logging_level,
                        format=log_format)


def log_url(
        server: "tornado.httpserver.HTTPServer"
) -> None:
    """Log the URL to console that the server is associated with."""
    port = list(server._sockets.values())[0].getsockname()[1]
    url = "http://localhost:%s" % port
    logging.log(100, "The web server is running at this URL: \n%s", url)


def stop_application(
        sockets: t.List["tornado.websocket.WebSocketHandler"]
) -> None:
    """Stop the application and any running threads / sockets."""
    logging.debug('Stopping...')
    tornado.ioloop.IOLoop.instance().stop()

    while len(sockets):
        logging.debug('Closing socket...')
        sockets.pop().close()

    for th in threading.enumerate():
        if th is not threading.main_thread() \
                and not th.name.startswith('pydevd'):
            logging.debug('Waiting for thread: %s' % th.name)
            th.join(timeout=5.0)
            if th.is_alive():
                logging.error('Failed to join thread: %s' % th.name)

    logging.debug('Exiting main')
