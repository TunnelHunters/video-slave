from picamera import PiCamera
from socket import socket, error
from time import sleep

# constants for video stuff
width = 854
height = 480
framerate = 32

# constants/variables for connection stuff
HOST = 'localhost'
PORT = 8082
connected = False

# socket to thing we're sending video shit to
client_socket = socket()
# retry connection every 5 seconds until success
while not connected:
    try:
        client_socket.connect((HOST, PORT))
        connected = True
    except error:
        print 'Connection to {}:{} failed, trying again in 5 seconds.'.format(HOST, PORT)
        sleep(5)

# this gets passed to the video function to be used as the destination for the stream
connection = client_socket.makefile('wb')
print 'Connected to master process!'

with PiCamera() as camera:
    camera.resolution = (width, height)
    camera.framerate = framerate
    camera.start_recording(connection, format='mjpeg')
    # TODO: How do I record forever?
    camera.wait_recording(60)
    camera.stop_recording()

connection.close()
client_socket.close()
