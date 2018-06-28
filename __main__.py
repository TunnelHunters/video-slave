from picamera import PiCamera
from socket import socket

HOST = 'localhost'
PORT = 8082

# socket to thing we're sending video shit to
client_socket = socket()
client_socket.connect((HOST, PORT))
connection = client_socket.makefile('wb')

with PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 1
    camera.start_recording(connection, format='mjpeg')
    camera.wait_recording(60)
    camera.wait_recording(60)
    camera.stop_recording()

connection.close()
client_socket.close()
