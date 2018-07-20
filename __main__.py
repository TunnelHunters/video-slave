import logging
from socketIO_client_nexus import SocketIO, LoggingNamespace
from lib.VideoThread import VideoThread

logger = logging.getLogger('socketIO-client')
logger.setLevel(logging.DEBUG)
logging.basicConfig()

HOST = 'localhost'
PORT = 8000


class ControlNamespace(LoggingNamespace):
    video_thread = None

    def on_connect(self):
        logger.debug('Socket.io connected to server!!')

    def on_start_video(self):
        if self.video_thread is not None:
            logger.error('Video thread already running.')
            return

        logger.debug('starting video thread')
        self.video_thread = VideoThread()
        self.video_thread.start()

    def on_stop_video(self):
        if self.video_thread is None:
            logger.error('Video thread isn\'t running, there\'s nothing to stop!')
            return

        logger.debug('Stopping video thread...')
        # block until thread is stopped+
        self.video_thread.stop()
        logger.debug('Video thread stopped!')
        self.video_thread = None


io = SocketIO(HOST, PORT)
io.define(ControlNamespace, '/robot')
io.wait()
