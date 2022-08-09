# EasyWallbox Free2Move Python Mqtt Manager / Monitor

**What is this?**

The EasyWallbox worked fine for me until I installed FV Roof Panels on my house and I want to use the solar excedents to charge my car during the day.

On the EB configuration I can set the charge limit, the safe and the DPM limit

*DPM = Dynamic Power Management*

But the DPM only works to balance the charging between the house consumption and the setted charge/safe limit.

What I need it's top ballance the charging between the Panels, house consumption and the DPM, at this point I am able to know how many kWh I get from the Panels and how many kWH I use at the house, so I have 2 options:

1. Buy a new Wallbox that it's able to do what I need, but this will cost me at least 800€
2. Connect to the Wallbox via BLE and change the safe or charge limit according to how many electricity I get from my Panels, for this I need to buy a bluetooth adapter for my HAL9000 and this will cost me a 8€


---

## How to connect, read and write information to the Wallbox

#### 1. Search for the BLE mac address.

Open your linux terminal and run :

```
hcitool dev
```

If you don't get any info you have to reinsert the Bluetooth dongle

Now run a low energy scan to get all the available BLE devices:

```
sudo hcitool lescan
```


At this point you get you Wallbox mac address in this format 00:00:00:00:00 (save it for later)


#### 2. Get the PIN code to connect to your wallbox (SPOILER: NO I'TS NOT 001234)

To connect with your android/ios device you have to scan a QR Code that's it's available on a sticker inside your Wallbox and after that probabilly you get a message in the app telling you the pin code it's 001234, no, it's not this code it's only to use it trought the official app.

How to get your code.

Open your camera / QR Code reader and point it to the sticker. You will get something like:

BT:N:2911AA00101728;M:F2ME.EWE08APEFXX;D:eWB01728;P:001234;A:9844;;

Let's decode it:

N: Serial               2911AA00101728
M: Part Number          F2ME.EWE08APEFXX
D: BT Name              eWB01728
P: Device Pin           001234
A: BLE Pin              9844

We need the A: value, in my case it's "9844" (save it for later)

## MQTT Commands ##

easywallbox/dpm 

| Description    | MQTT Command  |
|----------------| ------------- |
| Turn On DPM    | easywallbox/dpm/on |
| Turn Off DPM   | easywallbox/dpm/off | 
| Get Limit      | easywallbox/dpm/limit | 
| Set Limit      | easywallbox/dpm/limit/*{limit}* | 
| Get DPM status | easywallbox/dpm/status | 


easywallbox/charge

| Description          | MQTT Command  |
|----------------------| ------------- |
| Start Charge Now     | easywallbox/charge/start |
| Start Charge Delayed | easywallbox/charge/start/*{delay}* |
| Stop Charge Now      | easywallbox/charge/stop |
| Stop Charge Delayed  | easywallbox/charge/stop/*{delay}* |

easywallbox/limit

| Description    | MQTT Command  |
|----------------| ------------- |
| Get DPM Limit  | easywallbox/limit/dpm |
| Set DPM Limit  | easywallbox/limit/dpm/*{limit}* |
| Get Safe Limit | easywallbox/limit/safe |
| Set Safe Limit | easywallbox/limit/safe/*{limit}* |
| Get User Limit | easywallbox/limit/user |
| Set User Limit | easywallbox/limit/user/*{limit}* |

easywallbox/read

| Description               | MQTT Command  |
|---------------------------| ------------- |
| Read Manufacturing Values | easywallbox/read/manufacturing |
| Read Settings             | easywallbox/read/settings |
| Read App Data             | easywallbox/read/app_data |
| Read HW Settings          | easywallbox/read/hw_settings |
| Read Supply Voltage       | easywallbox/read/voltage |

All the responses are sent to MQTT under **easywallbox/message**

## Edit docker-compose.yaml

Update the file with your values

easywallbox:
    container_name: easywallbox
    restart: unless-stopped
    image: easywallbox:latest
    user: root
    environment:
      - MQTT_HOST=192.168.2.70
      - WALLBOX_ADDRESS = "00:00:00:00:00"
      - WALLBOX_PIN = "9844"


## BLE Available commands

**Login / Logout**

| Description | Command |
|-------------| ------------- |
| LOGIN       | $BLE,AUTH,*{pin}*\n |
| LOGOUT      | $BLE,LOGOUT\n |


**Start / Stop Charge**

| Description  | Command |
|--------------| ------------- |
| START CHARGE | $CMD,CHARGE,START,*{delay}*\n 
| STOP CHARGE  | $CMD,CHARGE,STOP,*{delay}*\n  


**Read / Write Commands**

| Description            | Command |
| ---------------------- | ------------- |
| INDEX WRITE            | $EEP,WRITE,IDX,*{index}*\n |
| INDEX READ             | $EEP,READ,IDX,*{index}*\n |
| READ ALARMS            | $EEP,READ,AL,*{alarmnum}*\n |
| READ MANUFACTURING     | $EEP,READ,MF\n |
| READ CHARGING SESSIONS | $EEP,READ,SL,*{sessionnum}*\n |
| READ SETTINGS          | $EEP,READ,ST\n |
| READ APP DATA          | $DATA,READ,AD\n |
| READ HW SETTINGS       | $DATA,READ,HS\n |
| READ SUPPLY VOLTAGE    | $DATA,READ,SV\n |
| SET USER LIMIT         | $EEP,WRITE,IDX,174,*{limit}*\n |
| SET DPM LIMIT          | $EEP,WRITE,IDX,158,*{limit}*\n |
| SET SAFE LIMIT         | $EEP,WRITE,IDX,156,*{limit}*\n |
| SET DPM OFF            | $EEP,WRITE,IDX,178,0\n |
| SET DPM ON             | $EEP,WRITE,IDX,178,1\n |
| GET USER LIMIT         | $EEP,READ,IDX,174\n |
| GET DPM LIMIT          | $EEP,READ,IDX,158\n |
| GET SAFE LIMIT         | $EEP,READ,IDX,156\n |
| GET DPM STATUS         | $EEP,READ,IDX,178\n |



