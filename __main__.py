import atexit
from os import environ
from socket import socket as _socket, AF_UNIX, SOCK_STREAM, error
from time import sleep
from picamera import PiCamera

# constants for video stuff
width = 854
height = 480
framerate = 32
# path to unix socket
socket_path = environ['THZ_videoSocket']
connected = False


@atexit.register
def on_exit():
    try:
        sock_fd.close()
        socket.close()
    except NameError:
        pass

    print 'Goodbye!!'

# socket we send frames through
socket = _socket(AF_UNIX, SOCK_STREAM)
# retry connection every 5 seconds until success
while not connected:
    try:
        socket.connect(socket_path)
        connected = True
    except error:
        print 'Connection to {} failed, trying again in 5 seconds.'.format(socket_path)
        sleep(5)

print 'Connected to {}!'.format(socket_path)
sock_fd = socket.makefile()

# PiCamera stuff
with PiCamera() as camera:
    camera.resolution = (width, height)
    camera.framerate = framerate
    camera.start_recording(sock_fd, format='mjpeg')
    # TODO: How do I record forever?
    camera.wait_recording(60)
    camera.stop_recording()
