
import blemap as bmap

def limit(arg):
    if(arg):
        limitValue = arg * 10
        return bmap.WALLBOX_EPROM["SET_DPM_LIMIT"].format(limit = str(limitValue))
    else:
        return bmap.WALLBOX_EPROM["GET_DPM_LIMIT"]



MQTT2BLE = {
    "easywallbox/dpm" : {
        "on" : bmap.WALLBOX_EPROM["SET_DPM_ON"],
        "off" : bmap.WALLBOX_EPROM["SET_DPM_OFF"],
        "limit" : limit, #limit/X (set) limit (get)
        "status" : bmap.WALLBOX_EPROM["GET_DPM_STATUS"] #get status
    }
}


