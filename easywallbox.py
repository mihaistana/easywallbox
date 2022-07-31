import sys
import asyncio
import commands as commands

from bleak import BleakClient

ADDRESS = "8C:F6:81:AD:B8:3E" #MAC ADDESS easywallbox

BLUETOOTH_WALLBOX_RX = "a9da6040-0823-4995-94ec-9ce41ca28833";
BLUETOOTH_WALLBOX_SERVICE = "331a36f5-2459-45ea-9d95-6142f0c4b307";
BLUETOOTH_WALLBOX_ST = "75A9F022-AF03-4E41-B4BC-9DE90A47D50B";
BLUETOOTH_WALLBOX_TX = "a73e9a10-628f-4494-a099-12efaf72258f";
BLUETOOTH_WALLBOX_UUID ="0A8C44F5-F80D-8141-6618-2564F1881650";

rx_buffer = "";
st_buffer = "";

def handle_rx(_: int, data: bytearray):
    global rx_buffer
    rx_buffer += data
    if "\n" in rx_buffer:
        print("rx received:", rx_buffer)
        rx_buffer = "";

def handle_st(_: int, data: bytearray):
    st_buffer = st_buffer + data
    if "\n" in st_buffer:
        print("st received:", st_buffer)
        st_buffer = "";

def handle_disconnect(_: BleakClient):
    print("Device was disconnected, goodbye.")
    # cancelling all tasks effectively ends the program
    for task in asyncio.all_tasks():
        task.cancel()

async def easywallbox(address):

    #async with BleakClient(address, disconnected_callback=handle_disconnect) as client:
    async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected}")

        paired = await client.pair(protection_level=2)
        print(f"Paired: {paired}")

        await client.start_notify(BLUETOOTH_WALLBOX_TX, handle_rx) #TX NOTIFY
        print("TX NOTIFY STARTED")
        #await client.start_notify(BLUETOOTH_WALLBOX_ST, handle_st) #ST NOTIFY (CANAL BUSMODE)
        #print("ST NOTIFY STARTED")

        data = bytes(commands.authBle("9844"),"utf-8")
        await client.write_gatt_char(BLUETOOTH_WALLBOX_RX, data)
        print("sent:", data)

        await asyncio.sleep(5)
        

if __name__ == "__main__":
    #try:
    asyncio.run(easywallbox(sys.argv[1] if len(sys.argv) == 2 else ADDRESS))
    #except asyncio.CancelledError:
        # task is cancelled on disconnect, so we ignore this error
    #    pass