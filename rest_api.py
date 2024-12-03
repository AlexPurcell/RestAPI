from phew import server, connect_to_wifi
from utime import sleep
from machine import Pin
import os
from dotenv import load_dotenv, dotenv_values
import json

ip = connect_to_wifi(os.getenv("HOST"), os.getenv("KEY"))

led_green = Pin(0, Pin.OUT)
led_red = Pin(1, Pin.OUT)

@server.route("/api/temperature", methods=["GET"])
def get_temperature(request):
    adc = machine.ADC(4)
    conversion_factor = 3.3 / (65535)
    sensor_value = adc.read_u16() * conversion_factor
    temperature = 27 - (sensor_value - 0.706) / 0.001721
    
    return json.dumps({"temperature" : temperature}), 200, {"Content-Type": "application/json"}

@server.route("/api/control-led", methods=["POST"])
def ledCommand(request):
    led_red.value(request.data["ledRed"])
    led_green.value(request.data["ledGreen"])
    return json.dumps({"message" : "Command sent successfully!"}), 200, {"Content-Type": "application/json"}

@server.catchall()
def catchall(request):
    return json.dumps({"message" : "URL not found!"}), 404, {"Content-Type": "application/json"}

server.run()