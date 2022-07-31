#!/usr/bin/env python3
import asyncio
import sys
from bleak import BleakClient
import paho.mqtt.client as mqtt
import os
import commands
import mqttmap
import time
import random
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)

mqttClient = None

class EasyWallbox:

    WALLBOX_ADDRESS = os.getenv('WALLBOX_ADDRESS', '8C:F6:81:AD:B8:3E')
    WALLBOX_PIN = os.getenv('WALLBOX_PIN', '9844')

    WALLBOX_RX = "a9da6040-0823-4995-94ec-9ce41ca28833";
    WALLBOX_SERVICE = "331a36f5-2459-45ea-9d95-6142f0c4b307";
    WALLBOX_ST = "75A9F022-AF03-4E41-B4BC-9DE90A47D50B";
    WALLBOX_TX = "a73e9a10-628f-4494-a099-12efaf72258f";
    WALLBOX_UUID ="0A8C44F5-F80D-8141-6618-2564F1881650";

    def __init__(self, queue):
        self._client = BleakClient(self.WALLBOX_ADDRESS)
        self._queue = queue

    def is_connected(self):
        return self._client.is_connected()

    async def write(self, data):
        if isinstance(data, str):
            data = bytearray(data, 'utf-8')
        await self._client.write_gatt_char(self.WALLBOX_RX, data)
        log.info("ble write: %s", data)

    async def connect(self):
        log.info("Connecting BLE...")
        await self._client.connect()
        log.info(f"Connected on {self.WALLBOX_ADDRESS}: {self._client.is_connected}")

    async def pair(self):
        log.info("Pairing BLE...")
        paired = await self._client.pair(protection_level=2)
        log.info(f"Paired: {paired}")

    async def start_notify(self):
        await self._client.start_notify(self.WALLBOX_TX, self._notification_handler_rx) #TX NOTIFY
        log.info("TX NOTIFY STARTED")
        await self._client.start_notify(self.WALLBOX_ST, self._notification_handler_st) #ST NOTIFY (CANAL BUSMODE)
        log.info("ST NOTIFY STARTED")


    

    _notification_buffer_rx = ""
    def _notification_handler_rx(self, sender, data):
        global client
        self._notification_buffer_rx += data.decode()
        if "\n" in self._notification_buffer_rx:
            log.info("_notification RX received: %s", self._notification_buffer_rx)

            if (client):
                client.publish(topic="easywallbox/message", payload=self._notification_buffer_rx, qos=1, retain=False)
            #self._queue.put_nowait(self._notification_buffer_rx)
            self._notification_buffer_rx = "";

        #print(data.decode('utf-8'), end='', file=sys.stdout, flush=True)
        #self._queue.put_nowait(data.decode('utf-8'))

    _notification_buffer_st = ""
    def _notification_handler_st(self, sender, data):
        
        self._notification_buffer_st += data.decode()
        if "\n" in self._notification_buffer_st:
            log.info("_notification ST received: %s", self._notification_buffer_st)
            #self._queue.put_nowait(self._notification_buffer_st)
            self._notification_buffer_st = "";

        #print(data.decode('utf-8'), end='', file=sys.stdout, flush=True)
        #self._queue.put_nowait(data.decode('utf-8'))

async def main():
    global client
    mqtt_host = os.getenv('MQTT_HOST', '192.168.2.70')
    mqtt_port = os.getenv('MQTT_PORT', 1883)
    mqtt_username = os.getenv('MQTT_PORT', "")
    mqtt_password = os.getenv('MQTT_PORT', "")

    
    queue = asyncio.Queue()

    eb = EasyWallbox(queue)
    await eb.connect()
    await eb.pair()
    await eb.start_notify()

    log.info("BLE AUTH START: %s", eb.WALLBOX_PIN)
    await eb.write(commands.authBle(eb.WALLBOX_PIN))

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected to MQTT Broker with result code "+str(rc))
        client.connected_flag=True
        log.info("Connected to MQTT Broker!")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe([("easywallbox/dpm",0), ("easywallbox/start",0), ("easywallbox/stop",0), ("easywallbox/limit",0)])

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        #print(msg.topic+" "+str(msg.payload))
        #queue.put_nowait(msg.payload)

        topic = msg.topic
        message = msg.payload.decode()
        log.info(f"Message received [{topic}]: {message}")
        ble_command = None

        try:
            if("/" in message):
                msx = message.split("/") limit/10
                ble_command = mqttmap.MQTT2BLE[topic][msx[0]](msx[1])
            else:
                ble_command = mqttmap.MQTT2BLE[topic][message]
        except Exception:
            pass

        print(ble_command)

        if(topic == "easywallbox/dpm"):

            if(message == "on"):
                queue.put_nowait(commands.setDpmOn())
            elif(message == "off"):
                queue.put_nowait(commands.setDpmOff())



    mqtt.Client.connected_flag=False

    client = mqtt.Client("mqtt-easywallbox")
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_start()
    client.username_pw_set(username=mqtt_username,password=mqtt_password)
    client.connect(mqtt_host, mqtt_port, 60)

    while not client.connected_flag: #wait in loop
        log.info("...")
        time.sleep(1)
    

    loop = asyncio.get_event_loop()

    #def read_line():
    #    line = sys.stdin.readline()
    #    if line:
    #        queue.put_nowait(line)

    #task = loop.add_reader(sys.stdin.fileno(), read_line)


    
    while True:
        if queue.empty():
           pass
        else:
            #item = await queue.get()
            item = queue.get_nowait()
            log.info("Consuming ...")
            if item is None:
                log.info("nothing to consume!")
                break
            log.info(f"Consuming item {item}...")
            await eb.write(item)
        await asyncio.sleep(1)

try:
    asyncio.run(main())
except asyncio.CancelledError:
    pass
#except Exception as e:
#    print(str(e), file=sys.stderr, flush=True)
#    sys.exit(1)