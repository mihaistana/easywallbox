
import blemap as bmap

def setDpmLimit(limit):
    limitValue = int(limit) * 10
    return bmap.WALLBOX_EPROM["SET_DPM_LIMIT"].format(limit = str(limitValue))

def setSafeLimit(limit):
    limitValue = int(limit) * 10
    return bmap.WALLBOX_EPROM["SET_SAFE_LIMIT"].format(limit = str(limitValue))

def setUserLimit(limit):
    limitValue = int(limit) * 10
    return bmap.WALLBOX_EPROM["SET_USER_LIMIT"].format(limit = str(limitValue))
    

def startCharge(delay=0):
    return bmap.WALLBOX_COMMANDS["START_CHARGE"].format(delay = str(delay))

def stopCharge(delay=0):
    return bmap.WALLBOX_COMMANDS["STOP_CHARGE"].format(delay = str(delay))

MQTT2BLE = {
    "easywallbox/dpm" : {
        "on" : bmap.WALLBOX_EPROM["SET_DPM_ON"],
        "off" : bmap.WALLBOX_EPROM["SET_DPM_OFF"],
        "limit" : bmap.WALLBOX_EPROM["GET_DPM_LIMIT"],
        "limit/" : setDpmLimit,
        "status" : bmap.WALLBOX_EPROM["GET_DPM_STATUS"] #get status
    },

    "easywallbox/charge" : {
        "start" : startCharge(0),
        "start/" : startCharge,
        "stop" : stopCharge(0),
        "stop/" : stopCharge,
    },

    "easywallbox/limit" : {
        "dpm" : setDpmLimit,
        "safe" : setSafeLimit,
        "user" : setUserLimit,
    }
}


