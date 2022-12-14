
WALLBOX_ANSWERS = { 
    "ANSWER_ERRAUTH" : "$ERR,AUTH\n", 
    "ANSWER_ERRBUSY" : "$ERR,BUSY\n", 
    "ANSWER_SYNTAX" : "$ERR,SYNTAX\n", 
    "ANSWER_AUTHFAIL" : "$BLE,AUTH,FAIL\n", 
    "ANSWER_AUTHOK" : "$BLE,AUTH,OK\n", 
    "ANSWER_WRITE_FAIL" : "$EEP,WRITE,FAIL\n", 
    "ANSWER_LOGOUT" : "$BLE,LOGOUT,OK\n" 
}

WALLBOX_BLE = { 
    "LOGIN" : "$BLE,AUTH,{pin}\n", 
    "LOGOUT" : "$BLE,LOGOUT\n" 
}

WALLBOX_COMMANDS = { 
    "START_CHARGE" : "$CMD,CHARGE,START,{delay}\n", 
    "STOP_CHARGE" : "$CMD,CHARGE,STOP,{delay}\n" 
}


WALLBOX_EPROM = { 
    "INDEX_WRITE" : "$EEP,WRITE,IDX\n",
    "INDEX_READ" : "$EEP,READ,IDX\n",
    "READ_ALARMS" : "$EEP,READ,AL\n",
    "READ_MANUFACTURING" : "$EEP,READ,MF\n",
    "READ_SESSIONS" : "$EEP,READ,SL\n",
    "READ_SETTINGS" : "$EEP,READ,ST\n",
    "READ_APP_DATA" : "$DATA,READ,AD\n",
    "READ_HW_SETTINGS" : "$DATA,READ,HS\n",
    "READ_SUPPLY_VOLTAGE" : "$DATA,READ,SV\n",

    "SET_USER_LIMIT" : "$EEP,WRITE,IDX,174,{limit}\n",
    "SET_DPM_LIMIT" : "$EEP,WRITE,IDX,158,{limit}\n",
    "SET_SAFE_LIMIT" : "$EEP,WRITE,IDX,156,{limit}\n",
    "SET_DPM_OFF" : "$EEP,WRITE,IDX,178,0\n",
    "SET_DPM_ON" : "$EEP,WRITE,IDX,178,1\n",

    "GET_USER_LIMIT" : "$EEP,READ,IDX,174\n",
    "GET_DPM_LIMIT" : "$EEP,READ,IDX,158\n",
    "GET_SAFE_LIMIT" : "$EEP,READ,IDX,156\n",
    "GET_DPM_STATUS" : "$EEP,READ,IDX,178\n"
}



