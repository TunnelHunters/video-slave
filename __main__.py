import atexit
from os import unlink, path
from socket import socket, AF_UNIX, SOCK_STREAM
from picamera import PiCamera

# constants for video stuff
width = 854
height = 480
framerate = 32
# path to unix socket
socket_path = '/tmp/THZ_video.sock'


@atexit.register
def on_exit():
    try:
        client_fd.close()
        client.close()
    except NameError:
        pass

    delete_socket()
    print 'goodbye!!'


def delete_socket():
    if path.exists(socket_path):
        unlink(socket_path)

if __name__ == '__main__':
    delete_socket()
    # make & bind socket then listen for connections
    sock = socket(AF_UNIX, SOCK_STREAM)
    sock.bind(socket_path)
    sock.listen(1)
    print 'listening at {}'.format(socket_path)

    # accept a connection
    client, _ = sock.accept()
    client_fd = client.makefile()
    print 'somebody connected!!'

    # PiCamera stuff
    with PiCamera() as camera:
        camera.resolution = (width, height)
        camera.framerate = framerate
        camera.start_recording(client_fd, format='mjpeg')
        # TODO: How do I record forever?
        camera.wait_recording(60)
        camera.stop_recording()
