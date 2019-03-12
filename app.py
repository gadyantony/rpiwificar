
import io
import picamera
import logging
# import motors
import RPi.GPIO as GPIO
import socketserver
from threading import Condition
from http import server

motors.stop()

PAGE="""\
<html>
<head>
<title>Raspberry Pi - Surveillance Camera</title>
</head>
<style>
table ,td, tr {
		width: 30%;
}
</style>
<body>
<center><h1>Raspberry Pi - Surveillance Camera</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>
<table style="width:100%; max-width: 500px; height:300px;">
			<tr>
				<td>
					<form action="/1" method="POST">
						<input type="image" name="direction" src="/img/left.svg" value="left" style="float:left; width:80% ;">
						</br>
					</form>
				</td>
				<td>
					<form action="/2" method="POST">
						<input type="image" name="direction" src="/img/forward.svg" value="forward" style="float:left; width:80%;">
						</br>
					</form>
				</td>
				<td>

					<form action="/3" method="POST">
						<input type="image" name="direction" src="/img/right.svg" value="right" style="float:left; width:80%;">
						</br>
					</form>

				</td>
			</tr>
			<tr>
				<td>
					<form action="/4" method="POST">
						<input type="image" name="direction" src="/img/reverse.svg" value="reverse" style=" margin-left:80px; width:80%;">
						</br>
					</form>
				</td>
				<td>
					<form action="/5" method="POST">
						<input type="image" name="direction" src="/img/stop.svg" value="stop" style="margin-left:80px; width:80%;">
						</br>
					</form>
				</td>
			</tr>
		</table>

</body>
</html>
"""
class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 90
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
@app.route('/')
def index():

	return render_template('index.html', server_ip=server_ip)

@app.route('/<changepin>', methods=['POST'])
def reroute(changepin):

	changePin = int(changepin) 

	if changePin == 1:
		motors.turnLeft()
	elif changePin == 2:
		motors.forward()
	elif changePin == 3:
		motors.turnRight()
	elif changePin == 4:
		motors.backward()
	elif changePin == 5:
		motors.stop()
	else:
		print("Wrong command")

	response = make_response(redirect(url_for('index')))
	return(response)

app.run(debug=True, host='0.0.0.0', port=8000) 
