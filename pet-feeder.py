from datetime import datetime
import time
import schedule as s
from gpiozero import Servo
from time import sleep
from loguru import logger
import RPi.GPIO as GPIO
GPIO.setwarnings(False)



foodServoPin = Servo(17)
cleanServoPin = Servo(27)
drinkingWaterRelayPin = 23
cleaningWaterRelayPin = 24

GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
GPIO.setup(foodServoPin,GPIO.OUT)
GPIO.setup(cleanServoPin,GPIO.OUT)


GPIO.setup(drinkingWaterRelayPin,GPIO.OUT)
GPIO.setup(cleaningWaterRelayPin,GPIO.OUT)

GPIO.output(drinkingWaterRelayPin,GPIO.HIGH)
GPIO.output(cleaningWaterRelayPin,GPIO.HIGH)


foodServoPin.min()
cleanServoPin.mid()
sleep(0.5)
       

def cleanBowl():
    GPIO.output(cleaningWaterRelayPin,GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(cleaningWaterRelayPin,GPIO.HIGH)
    time.sleep(0.5)
    logger.debug("Cleaning the bowl")
    cleanServoPin.max()
    time.sleep(1)
    cleanServoPin.mid()
    time.sleep(1)
    logger.debug("Emptying the bowl")       

def operateFood():
    cleanBowl()
    time.sleep(1)
    logger.debug("Serving Food!")
    foodServoPin.max()
    time.sleep(2)
    foodServoPin.min()
    time.sleep(2)
    logger.debug("Food Served!")


def operateWater():
    cleanBowl()
    logger.debug("Serving Drinkng Water")
    GPIO.output(drinkingWaterRelayPin,GPIO.LOW)
    time.sleep(2)
    GPIO.output(drinkingWaterRelayPin,GPIO.HIGH)
    time.sleep(2)
    
 



s.every().day.at("09:00").do(operateFood)
logger.debug("Feeding the pet!!")
s.every().day.at("09:30").do(operateWater)
logger.debug("Providing Drinking Water")
s.every().day.at("10:00").do(cleanBowl)   
logger.debug("Cleaning the Bowl") 

try:
    while(1):
        now = datetime.now()
        curr_time = now.strftime("%H:%M:%S")
        h, _, _ = curr_time.split(":")
        s.run_pending()


except KeyboardInterrupt:
    GPIO.cleanup()
    exit(0)
