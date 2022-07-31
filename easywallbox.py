#!/usr/bin/env python3
import paho.mqtt.client
import time
import sys
import asyncio
import commands as commands
import os
from bleak import BleakClient

import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)

ble_address = os.getenv('BLE_ADDRESS', '8C:F6:81:AD:B8:3E')
ble_pin = os.getenv('BLE_PIN', '9844')

BLUETOOTH_WALLBOX_RX = "a9da6040-0823-4995-94ec-9ce41ca28833";
BLUETOOTH_WALLBOX_SERVICE = "331a36f5-2459-45ea-9d95-6142f0c4b307";
BLUETOOTH_WALLBOX_ST = "75A9F022-AF03-4E41-B4BC-9DE90A47D50B";
BLUETOOTH_WALLBOX_TX = "a73e9a10-628f-4494-a099-12efaf72258f";
BLUETOOTH_WALLBOX_UUID ="0A8C44F5-F80D-8141-6618-2564F1881650";

mqtt_host = os.getenv('MQTT_HOST', '192.168.2.70')
mqtt_port = os.getenv('MQTT_PORT', 1883)
mqtt_username = os.getenv('MQTT_PORT', "")
mqtt_password = os.getenv('MQTT_PORT', "")

def mqtt_on_connect(client, userdata, flags, rc):
    # This will be called once the client connects
    if rc == 0:
        client.connected_flag=True
        log.info("Connected to MQTT Broker!")
        mqtt_subscribe(client)
    else:
        log.info("Failed to connect, return code %d\n", rc)
    

def mqtt_subscribe(client):
    client.subscribe([("easywallbox/dpm",0), ("easywallbox/start",0), ("easywallbox/stop",0), ("easywallbox/limit",0)])

def mqtt_on_message(client, userdata, msg):
    log.info(f"Message received [{msg.topic}]: {msg.payload}")
    topic = msg.topic
    message = msg.payload.decode()
    if(topic == "easywallbox/dpm"):
        if(message == "on"):
            ble_send_rx(commands.setDpmOn())
            #data = bytes(commands.setDpmOff,"utf-8")
            #await ble_client.write_gatt_char(BLUETOOTH_WALLBOX_RX, data)


async def ble_send_rx(data):
    global ble_client 
    data = bytes(data,"utf-8")
    await ble_client.write_gatt_char(BLUETOOTH_WALLBOX_RX, data)
    log.info("ble sent: %s", data)

rx_buffer = "";
st_buffer = "";


def ble_handle_rx(_: int, data: bytearray):
    global rx_buffer
    rx_buffer += data.decode()
    if "\n" in rx_buffer:
        log.info("rx received: %s", rx_buffer)
        clientMQTT.publish(topic="easywallbox/message", payload=rx_buffer, qos=1, retain=False)
        rx_buffer = "";

def ble_handle_st(_: int, data: bytearray):
    global st_buffer
    st_buffer += data.decode()
    if "\n" in st_buffer:
        log.info("st received: %s", st_buffer)
        st_buffer = "";

def ble_handle_disconnect(_: BleakClient):
    log.info("Device was disconnected, goodbye.")
    # cancelling all tasks effectively ends the program
    for task in asyncio.all_tasks():
        task.cancel()

async def easywallbox():

    log.info("Connecting BLE...")
    #async with BleakClient(ble_address, disconnected_callback=ble_handle_disconnect) as ble_client:
    async with BleakClient(ble_address) as client:
        global ble_client 
        ble_client = client;
        log.info(f"Connected: {ble_client.is_connected}")

        paired = await ble_client.pair(protection_level=2)
        log.info(f"Paired: {paired}")

        await ble_client.start_notify(BLUETOOTH_WALLBOX_TX, ble_handle_rx) #TX NOTIFY
        log.info("TX NOTIFY STARTED")
        await ble_client.start_notify(BLUETOOTH_WALLBOX_ST, ble_handle_st) #ST NOTIFY (CANAL BUSMODE)
        log.info("ST NOTIFY STARTED")

        log.info("BLE AUTH START: %s", ble_pin)
        
        await ble_send_rx(commands.authBle(ble_pin))
        await asyncio.sleep(5)

        while True:
            time.sleep(1)
            #loop forever

        
        





#clientMQTT.loop_stop()
if __name__ == "__main__":
    try:
        paho.mqtt.client.Client.connected_flag=False#create flag in class

        clientMQTT = paho.mqtt.client.Client("mqtt-easywallbox") # client ID "mqtt-test"
        clientMQTT.on_connect = mqtt_on_connect
        clientMQTT.on_message = mqtt_on_message
        clientMQTT.loop_start()
        log.info("Connecting to MQTT broker: %s ",mqtt_host)
        clientMQTT.username_pw_set(username=mqtt_username,password=mqtt_password)
        clientMQTT.connect(mqtt_host, mqtt_port)
        #clientMQTT.loop_forever()  # Start networking daemon

        while not clientMQTT.connected_flag: #wait in loop
            log.info("...")
        time.sleep(1)

        asyncio.run(easywallbox())

        clientMQTT.loop_stop()

    except asyncio.CancelledError:
        # task is cancelled on disconnect, so we ignore this error
        pass