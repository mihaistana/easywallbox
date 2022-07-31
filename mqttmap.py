
import blemap as bmap

def limit_dpm(arg):
    limitValue = int(arg) * 10
    return bmap.WALLBOX_EPROM["SET_DPM_LIMIT"].format(limit = str(limitValue))


MQTT2BLE = {
    "easywallbox/dpm" : {
        "on" : bmap.WALLBOX_EPROM["SET_DPM_ON"],
        "off" : bmap.WALLBOX_EPROM["SET_DPM_OFF"],
        "limit" : bmap.WALLBOX_EPROM["GET_DPM_LIMIT"],
        "limit/" : limit_dpm,
        "status" : bmap.WALLBOX_EPROM["GET_DPM_STATUS"] #get status
    }
}


