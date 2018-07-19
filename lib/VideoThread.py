import logging
from time import sleep
from threading import Thread, Event
from http.client import HTTPConnection

logger = logging.getLogger('video_thread')
logger.setLevel(logging.DEBUG)

# TODO: make HOST an environment variable
HOST = 'localhost'
PORT = 8000


# TODO: this is a palceholder for the Picam function
class Spamera:
    data = b'dungus'

    def start_recording(self, custom_output):
        while True:
            custom_output.write(self.data)
            sleep(0.01)


def chunkify(data):
    return b'%i\r\n%s\r\n' % (len(data), data)


class StopTime(Exception):
    def __init__(self):
        super(Exception, self).__init__('TIME TO STOP')


class VideoThread(Thread):
    connection = HTTPConnection(HOST, PORT)
    camera = Spamera()
    stop_event = Event()

    def __init__(self):
        super().__init__()
        # unset stop_event (because aparently it doesn't do this itself)
        self.stop_event.clear()
        # set up connection
        self.connection.connect()
        self.connection.putrequest('PUT', '/')
        self.connection.putheader('Transfer-Encoding', 'chunked')
        self.connection.endheaders()

    def run(self):
        logger.debug('thread started!')
        # start recording until a StopTime exception is thrown in the custom_output
        try:
            """
            THIS IS THE ONLY SHIT THE THREAD DOES (send video)
            any connection setup or tear-down happens outside the thread
            """
            self.camera.start_recording(self)
        except StopTime:
            pass

    def write(self, data):
        if self.stop_event.is_set():
            logger.debug('STOP TIME!!!')
            raise StopTime()

        self.connection.send(chunkify(data))

    def stop(self):
        self.stop_event.set()
        # wait for thread to terminate
        self.join()
        self.connection.send(b'0\r\n\r\n')
        self.connection.getresponse().read()
