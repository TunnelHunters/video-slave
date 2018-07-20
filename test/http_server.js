const http = require('http');
const io = require('socket.io');

const server = http.createServer((req, res) => {
	req.on('data', data => console.log(data.toString()));
	req.on('end', () => res.end());
});
server.on('clientError', error => {
	console.error(error);
	if (error.message !== 'Parse Error' || !error.hasOwnProperty('rawPacket'))
		return;

	console.error(error.rawPacket.toString())
});

const ioServer = new io(server)
	.of('/robot')
	.on('connection', socket => {
		console.log('socket.io client connected!!');
		stopWithoutStart(socket);
	});

server.listen(8000, () => console.log('http listening!!'));

function startWithoutStop(socket) {
	socket.emit('start_video');
	setTimeout(() => socket.emit('start_video'), 2500);
	setTimeout(() => socket.emit('stop_video'), 5000);
}

function stopWithoutStart(socket) {
	socket.emit('stop_video');
	setTimeout(() => socket.emit('start_video'), 1000);
	setTimeout(() => socket.emit('stop_video'), 2000);
	setTimeout(() => socket.emit('stop_video'), 3000);
}
