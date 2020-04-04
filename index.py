import urllib
import json
import kernel
import time
import RPi.GPIO as GPIO
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
#GPIO.setup(16, GPIO.OUT)

def get_state():
    url = "http://www.deepthinkai.top:8000/IOT?NO=IOT001&state=get"
    res = {'control':'OFF', 'hour':0, 'mimute':0}
    try:
        f = urllib.request.urlopen(url)
        content = f.read()
        res = json.loads(content)
       # print(res)
    except:
        pass
    return res

def start():
    while True:
        data=get_state()
        dt = list(time.localtime())  
        hour = dt[3]  
        minute = dt[4]  
        if hour == data['hour'] and minute == data['minute'] and data['control']=='ON':
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(16, GPIO.OUT)
            GPIO.output(16, GPIO.HIGH)
            logger.info("GPIO16 is high")
            kernel.playmusic('back.mp3',20)
            logger.info("play music 20s")
            kernel.read_weather(data['city'])
            logger.info("play weather")
            kernel.playmusic('back.mp3',5)
            logger.info("play music 5s")
            kernel.read_news('junshi',5)
            logger.info("play news")
            GPIO.output(16, GPIO.LOW)
            GPIO.cleanup()
            logger.info("GPIO16 is low")
            kernel.playmusic('back.mp3',30)
        time.sleep(5)


if __name__=="__main__":
    start()
