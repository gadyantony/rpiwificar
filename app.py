import RPi.GPIO as GPIO
from flask import Flask 
GPIO.setmode(GPIO.BOARD)
import motors
import socket