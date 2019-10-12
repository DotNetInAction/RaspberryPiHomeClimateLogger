import time
import board
import busio
import adafruit_sgp30
import Adafruit_DHT
import requests

URL = "http://192.168.1.11:3005"

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

print("SGP30 serial #", [hex(i) for i in sgp30.serial])

sgp30.iaq_init()
sgp30.set_iaq_baseline(0x8973, 0x8aae)

elapsed_sec = 0

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
    else:
        humidity, temperature = 0

    print("eCO2 = %d ppm \t TVOC = %d ppb" % (sgp30.eCO2, sgp30.TVOC))
    
    requests.get(url = URL, params = {'room':'main', 'sensor':'temperature','temp':temperature})
    requests.get(url = URL, params = {'room':'main', 'sensor':'humidity','temp':humidity})
    requests.get(url = URL, params = {'room':'main', 'sensor':'co2','temp':sgp30.eCO2})
    requests.get(url = URL, params = {'room':'main', 'sensor':'voc','temp':sgp30.TVOC})
    
    time.sleep(3)    
