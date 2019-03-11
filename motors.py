import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
import time

# Pin# not GPIo
Motor1A = 20
Motor2A = 21


GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor2A,GPIO.OUT)

def backward():
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor2A,GPIO.HIGH)
        
def forward():
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor2A,GPIO.LOW)
        
def turnLeft():
        print("Going Left")
        GPIO.output(Motor1A,GPIO.HIGH)
        GPIO.output(Motor2A,GPIO.LOW)
        
def turnRight():
        print("Going Right")
        GPIO.output(Motor1A,GPIO.LOW)
        GPIO.output(Motor2A,GPIO.HIGH)
       
def stop():
	print("Stopping")
	GPIO.output(Motor1A,GPIO.LOW)
	GPIO.output(Motor2A,GPIO.LOW)