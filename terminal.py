import sys
import asyncio

from bleak import BleakClient

ADDRESS = "8C:F6:81:AD:B8:3E" #MAC ADDESS easywallbox

BLUETOOTH_WALLBOX_RX = "a9da6040-0823-4995-94ec-9ce41ca28833";
BLUETOOTH_WALLBOX_SERVICE = "331a36f5-2459-45ea-9d95-6142f0c4b307";
BLUETOOTH_WALLBOX_ST = "75A9F022-AF03-4E41-B4BC-9DE90A47D50B";
BLUETOOTH_WALLBOX_TX = "a73e9a10-628f-4494-a099-12efaf72258f";
BLUETOOTH_WALLBOX_UUID ="0A8C44F5-F80D-8141-6618-2564F1881650";

BLUETOOTH_WALLBOX_DEVICE_INFO = "0000180a-0000-1000-8000-00805f9b34fb";
# $EEP,READ,IDX\n
# $DATA,READ,AD

SET_DPM_LIMIT_1 = "$EEP,WRITE,IDX,158,10\n"
SET_USER_LIMIT_1 = "$EEP,WRITE,IDX,174,80\n" #220 => 22.0A
SET_DPM_OFF = "$EEP,WRITE,IDX,178,0\n";
SET_DPM_ON = "$EEP,WRITE,IDX,178,1\n";

BLE_AUTH = b'$BLE,AUTH,9844\n'

def handle_rx(_: int, data: bytearray):
        print("received:", data)

def handle_disconnect(_: BleakClient):
        print("Device was disconnected, goodbye.")
        # cancelling all tasks effectively ends the program
        for task in asyncio.all_tasks():
            task.cancel()

async def wallbox_terminal(address):

    async with BleakClient(address, disconnected_callback=handle_disconnect) as client:
    #async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected}")

        
        await client.write_gatt_char(BLUETOOTH_WALLBOX_SERVICE, BLE_AUTH)
        print("sent:", BLE_AUTH)

        paired = await client.pair(protection_level=2)
        print(f"Paired: {paired}")

        await client.start_notify(BLUETOOTH_WALLBOX_TX, handle_rx)


        print("Type command and press ENTER...")

        loop = asyncio.get_running_loop()

        while True:
            # This waits until you type a line and press ENTER.
            # A real terminal program might put stdin in raw mode so that things
            # like CTRL+C get passed to the remote device.
            data = await loop.run_in_executor(None, sys.stdin.buffer.readline)

            # data will be empty on EOF (e.g. CTRL+D on *nix)
            if not data:
                break

            # some devices, like devices running MicroPython, expect Windows
            # line endings (uncomment line below if needed)
            # data = data.replace(b"\n", b"\r\n")

            await client.write_gatt_char(BLUETOOTH_WALLBOX_RX, data)
            print("sent:", data)
        


if __name__ == "__main__":
    try:
        asyncio.run(wallbox_terminal(sys.argv[1] if len(sys.argv) == 2 else ADDRESS))
    except asyncio.CancelledError:
        # task is cancelled on disconnect, so we ignore this error
        pass