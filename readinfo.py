"""
Service Explorer
----------------
An example showing how to access and print out the services, characteristics and
descriptors of a connected GATT server.
Created on 2019-03-25 by hbldh <henrik.blidh@nedomkull.com>

INFO:__main__:[Service] 169b52a0-b7fd-40da-998c-dd9238327e55 (Handle: 31): Unknown
INFO:__main__:  [Characteristic] 12e868e7-c926-4906-96c8-a7ee81d4b1b3 (Handle: 36): Unknown (read), Value: b'vxeV33m\x0c\x9e\xb9\x1d\xfc\x8c\xf6\x81\xff\xfe\xad\xb8>'
INFO:__main__:  [Characteristic] 503a5d70-b443-466e-9aeb-c342802b184e (Handle: 34): Unknown (write-without-response,write), Value: None
INFO:__main__:  [Characteristic] 902ee692-6ef9-48a8-a430-5212eeb3e5a2 (Handle: 32): Unknown (write), Value: None
INFO:__main__:[Service] 331a36f5-2459-45ea-9d95-6142f0c4b307 (Handle: 21): Unknown
INFO:__main__:  [Characteristic] 75a9f022-af03-4e41-b4bc-9de90a47d50b (Handle: 28): Unknown (read,write-without-response,write,notify,indicate), Value: b'\x01'
INFO:__main__:      [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 30): Client Characteristic Configuration) | Value: b'\x00\x00'
INFO:__main__:  [Characteristic] a73e9a10-628f-4494-a099-12efaf72258f (Handle: 25): Unknown (write-without-response,notify,indicate), Value: None
INFO:__main__:      [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 27): Client Characteristic Configuration) | Value: b'\x00\x00'
INFO:__main__:  [Characteristic] a9da6040-0823-4995-94ec-9ce41ca28833 (Handle: 22): Unknown (write-without-response,write,notify), Value: None
INFO:__main__:      [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 24): Client Characteristic Configuration) | Value: b'\x00\x00'
INFO:__main__:[Service] 0000180a-0000-1000-8000-00805f9b34fb (Handle: 14): Device Information
INFO:__main__:  [Characteristic] 00002a26-0000-1000-8000-00805f9b34fb (Handle: 19): Firmware Revision String (read), Value: b'BGX13P.1.2.2045.0-1261-2045'
INFO:__main__:  [Characteristic] 00002a24-0000-1000-8000-00805f9b34fb (Handle: 17): Model Number String (read), Value: b'eWB'
INFO:__main__:  [Characteristic] 00002a29-0000-1000-8000-00805f9b34fb (Handle: 15): Manufacturer Name String (read), Value: b'Fimer'
INFO:__main__:[Service] 00001801-0000-1000-8000-00805f9b34fb (Handle: 1): Generic Attribute Profile
INFO:__main__:  [Characteristic] 00002b29-0000-1000-8000-00805f9b34fb (Handle: 7): Client Supported Features (read,write), Value: b'\x01'
INFO:__main__:  [Characteristic] 00002b2a-0000-1000-8000-00805f9b34fb (Handle: 5): Database Hash (read), Value: b'7W\xe4\x8a\xe9\xea\x90\r\x08\xa5\x15\xde\x8f\x8c?\xb1'
INFO:__main__:  [Characteristic] 00002a05-0000-1000-8000-00805f9b34fb (Handle: 2): Service Changed (indicate), Value: None
INFO:__main__:      [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 4): Client Characteristic Configuration) | Value: b'\x02\x00'

"""

import sys
import platform
import asyncio
import logging

from bleak import BleakClient

logger = logging.getLogger(__name__)

ADDRESS="8C:F6:81:AD:B8:3E"


async def main(address):
    async with BleakClient(address) as client:
        logger.info(f"Connected: {client.is_connected}")

        for service in client.services:
            logger.info(f"[Service] {service}")
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = bytes(await client.read_gatt_char(char.uuid))
                        logger.info(
                            f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}"
                        )
                    except Exception as e:
                        logger.error(
                            f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {e}"
                        )

                else:
                    value = None
                    logger.info(
                        f"\t[Characteristic] {char} ({','.join(char.properties)}), Value: {value}"
                    )

                for descriptor in char.descriptors:
                    try:
                        value = bytes(
                            await client.read_gatt_descriptor(descriptor.handle)
                        )
                        logger.info(f"\t\t[Descriptor] {descriptor}) | Value: {value}")
                    except Exception as e:
                        logger.error(f"\t\t[Descriptor] {descriptor}) | Value: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main(sys.argv[1] if len(sys.argv) == 2 else ADDRESS))