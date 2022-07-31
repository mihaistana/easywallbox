
import easywallbox.blemap as bmap


def setUserLimit(limit):
    
    limitValue = limit * 10
    return bmap.WALLBOX_EPROM["SET_USER_LIMIT"].format(limit = str(limitValue))
    
def setDpmLimit(limit):
    limitValue = limit * 10
    return bmap.WALLBOX_EPROM["SET_DPM_LIMIT"].format(limit = str(limitValue))

def setSafeLimit(limit):
    limitValue = limit * 10
    return bmap.WALLBOX_EPROM["SET_SAFE_LIMIT"].format(limit = str(limitValue))


def startCharge(delay=0):
    return bmap.WALLBOX_COMMANDS["START_CHARGE"].format(delay = str(delay))

def stopCharge():
    return bmap.WALLBOX_COMMANDS["STOP_CHARGE"]


def setDpmOff():
    return bmap.WALLBOX_EPROM["SET_DPM_OFF"]

def setDpmOn():
    return bmap.WALLBOX_EPROM["SET_DPM_ON"]


def authBle(pin="0000"): #9844 
    return bmap.WALLBOX_BLE["LOGIN"].format(pin = str(pin))

