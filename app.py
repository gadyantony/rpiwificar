
import io
import picamera
import logging
import motors
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