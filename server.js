const net = require('net');
const fs = require('fs');

const endOfFrame = Buffer.from([0xFF, 0xD9]);
const socket_path = '/tmp/THZ_video.sock';

const socket = net.createConnection(socket_path, () => console.log('connected to video slave'));
socket.on('data', processFrameData);

let accumulator = Buffer.alloc(0);
function processFrameData(data) {
	const frameEndIndex = data.indexOf(endOfFrame);
	// If there's an end of frame marker in the data,
	if (frameEndIndex !== -1) {
		// Concatenate the accumulator and everything in data up to (and including) the end of frame marker
		emitFrame(Buffer.concat([accumulator, data.slice(0, frameEndIndex + 2)]));
		// clear the accumulator
		accumulator = Buffer.alloc(0);
		// recusrive call on the rest of the data
		processFrameData(data.slice(frameEndIndex + 2, data.length));
		return;
	}
	// Otherwise just add everything to the accumulator
	accumulator = Buffer.concat([accumulator, data]);
}

function emitFrame(frame) {
	console.log(frame.length);
}
