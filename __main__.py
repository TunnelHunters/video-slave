import atexit
from os import unlink, path
from socket import socket, AF_UNIX, SOCK_STREAM, error
from picamera import PiCamera

# constants for video stuff
width = 854
height = 480
framerate = 32
# path to unix socket
socket_path = '/tmp/THZ_video.sock'


@atexit.register
def goodbye():
    # delete socket node on exit
    unlink(socket_path)
    print 'deleted {}'.format(socket_path)

if path.exists(socket_path):
    unlink(socket_path)

# makest, bindest, and listenest on thine socket
sock = socket(AF_UNIX, SOCK_STREAM)
sock.bind(socket_path)
sock.listen(1)
print 'listening at {}'.format(socket_path)

# accept a connection
client, client_address = sock.accept()
print 'connection from {}!!'.format(client_address)

# PiCamera stuff
with PiCamera() as camera:
    camera.resolution = (width, height)
    camera.framerate = framerate
    camera.start_recording(client.makefile(), format='mjpeg')
    # TODO: How do I record forever?
    camera.wait_recording(60)
    camera.stop_recording()

connection.close()
client_socket.close()
