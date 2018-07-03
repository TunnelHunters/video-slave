const net = require('net');
const fs = require('fs');

const endOfFrame = Buffer.from([0xFF, 0xD9]);

const server = net.createServer(socket => {
	console.log('somebody connected!');
	socket.on('data', data => {
		console.log(
			data.length,
			data.indexOf(startOfFrame),
			data.lastIndexOf(startOfFrame),
			data.indexOf(endOfFrame),
			data.lastIndexOf(endOfFrame)
		);
	});
});

let accumulator = Buffer.alloc(0);
function processFrameData(data) {
	const frameEndIndex = data.indexOf(endOfFrame);
	// If there's an end of frame marker in the data,
	if (frameEndIndex !== -1) {
		// Add everything up to end of frame marker (including end of frame marker) to the accumulator
		accumulator = Buffer.concat([accumulator, data.slice(0, frameEndIndex + 2)]);
		// do the thing with the frame
		emitFrame(accumulator);
		// srecusrive call on the rest of the data
		processFrameData(data.slice(frameEndIndex + 2, data.length))
	}
	// Otherwise just add everything to the accumulator
	accumulator = Buffer.concat([accumulator, data]);
}

function emitFrame(frame) {
	console.log(frame.length);
}

server.listen(8082, () => console.log('listening'));
