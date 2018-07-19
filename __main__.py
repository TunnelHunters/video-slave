import logging
from socketIO_client_nexus import SocketIO, BaseNamespace
from lib.VideoThread import VideoThread

logger = logging.getLogger('socketIO-client')
logger.setLevel(logging.DEBUG)
logging.basicConfig()

HOST = 'localhost'
PORT = 8000

"""
THE PLAN:
Socket.io connection to webserver
--- wait ---
Webserver: LET'S GO DADDY
Videoslav: OK YEAH
<-- HTTP request ---
<-- start streaming boi ---
Webserver: OK STOP PLS
Videoslav: YOU GOT IT
*** Stop streaming & close HTTP req? ***
"""


class ControlNamespace(BaseNamespace):
    video_thread = None

    def on_connect(self):
        logger.debug('socket.io connected to server!!')

    def on_start_video(self):
        if self.video_thread is not None:
            raise Exception('video thread already running')

        logger.debug('starting video thread')
        self.video_thread = VideoThread()
        self.video_thread.start()

    def on_stop_video(self):
        logger.debug('stopping video thread')
        # block until thread is stopped+
        self.video_thread.stop()
        logger.debug('video thread stopped!')
        self.video_thread = None

io = SocketIO(HOST, PORT)
io.define(ControlNamespace, '/robot')
io.wait()
