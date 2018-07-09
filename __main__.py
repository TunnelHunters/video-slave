import atexit
from os import environ
from socket import socket, AF_UNIX, SOCK_STREAM, error
from time import sleep
from picamera import PiCamera

# constants for video stuff
width = 854
height = 480
framerate = 32
# path to unix socket
socket_path = environ['THZ_videoSocket']


@atexit.register
def on_exit():
    try:
        sock_fd.close()
        sock.close()
    except NameError:
        pass

    print 'Goodbye!!'

if __name__ == '__main__':
    # make & bind socket then listen for connections
    sock = socket(AF_UNIX, SOCK_STREAM)
    try:
        sock.connect(socket_path)
    except error:
        print 'Connection to robot-master failed, trying again in 5 seconds.'
        sleep(5)

    print 'Connected to {}!'.format(socket_path)
    sock_fd = sock.makefile()

    # PiCamera stuff
    with PiCamera() as camera:
        camera.resolution = (width, height)
        camera.framerate = framerate
        camera.start_recording(sock_fd, format='mjpeg')
        # TODO: How do I record forever?
        camera.wait_recording(60)
        camera.stop_recording()
