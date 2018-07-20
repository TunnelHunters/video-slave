import logging
from time import sleep
from threading import Thread, Event
from http.client import HTTPConnection

logger = logging.getLogger('video_thread')
logger.setLevel(logging.DEBUG)

# TODO: make URL an environment variable
URL = 'localhost'
PORT = 8000


# TODO: this is a palceholder for the Picam function
class Spamera:
    data = b'dungus'

    def start_recording(self, custom_output):
        while True:
            custom_output.write(self.data)
            sleep(0.01)


class StopTime(Exception):
    def __init__(self):
        super(Exception, self).__init__('TIME TO STOP')


def chunkify(data):
    """
    Turn a piece of data into an HTTP chunked encoding chunk
    ex.
        Hello!
    becomes
        6\r\n
        Hello!\r\n
    """
    return b'%i\r\n%s\r\n' % (len(data), data)


class VideoThread(Thread):
    connection = HTTPConnection(URL, PORT)
    camera = Spamera()  # TODO: replace with picamera.PiCamera
    stop_event = Event()

    def run(self):
        """The actual thread."""
        logger.debug('thread started!')
        # Clear stop event flag because apparently instantiating a new object doesn't do that implicitly
        self.stop_event.clear()
        # Open PUT request with chunked encoding
        self.connection.connect()
        self.connection.putrequest('PUT', '/')
        self.connection.putheader('Transfer-Encoding', 'chunked')
        self.connection.endheaders()

        try:
            # Record indefinitely until StopTime exception is raised
            self.camera.start_recording(self)
        except StopTime:
            # Handle StopTime exception by continuing
            pass

        # End chunked encoding & close connetion properly with read() call
        self.connection.send(b'0\r\n\r\n')
        self.connection.getresponse().read()

    def write(self, data):
        """
        This is so we can pass the VideoThread object straight to picam.start_recording().
        When called, write data to HTTP connection. Raise StopTime exception if stop flag is set.
        """
        if self.stop_event.is_set():
            logger.debug('STOP TIME!!!')
            raise StopTime()

        self.connection.send(chunkify(data))

    def stop(self):
        """Set the stop flag and wait for the trhead to terminate."""
        self.stop_event.set()
        # wait for thread to terminate
        self.join()
