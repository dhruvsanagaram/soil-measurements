import asyncio
from bleak import BleakClient, BleakScanner

# Replace with your ESP32's BLE service and characteristic UUIDs
SERVICE_UUID = "12345678-1234-1234-1234-1234567890ab"
CHARACTERISTIC_UUID = "87654321-4321-4321-4321-0987654321ba"

SERVICE_UUID_PH = "12345678-5678-5678-5678-1234567890cd"
CHARACTERISTIC_UUID_PH = "87654321-8765-8765-8765-0987654321dc"

DEVICE_NAME = "ESP32_SPIFFS_BLE_Server"  # Name of your ESP32 BLE device


async def read_characteristic(client, characteristic_uuid, description):
    """
    Helper function to read and print data from a characteristic.
    """
    try:
        data = await client.read_gatt_char(characteristic_uuid)
        if data:
            print(f"{description}: {data.decode('utf-8')}")
        else:
            print(f"{description}: Received data is empty.")
    except Exception as e:
        print(f"Failed to read {description}: {e}")


async def main():
    # Scan for the BLE device
    print("Scanning for devices...")
    devices = await BleakScanner.discover()
    esp32_device = None

    for device in devices:
        if device.name and DEVICE_NAME in device.name:
            esp32_device = device
            print(f"Found ESP32 device: {device.name} - {device.address}")
            break

    if not esp32_device:
        print(f"Device '{DEVICE_NAME}' not found. Make sure the device is on and advertising.")
        return

    # Connect to the ESP32 BLE server
    async with BleakClient(esp32_device.address) as client:
        print(f"Connected to {esp32_device.name}")

        # Check if the required services are present
        services = await client.get_services()
        service_uuids = [service.uuid for service in services]

        if SERVICE_UUID not in service_uuids:
            print(f"Analog Service UUID {SERVICE_UUID} not found on device.")
        else:
            await read_characteristic(client, CHARACTERISTIC_UUID, "Analog Value")

        if SERVICE_UUID_PH not in service_uuids:
            print(f"pH Service UUID {SERVICE_UUID_PH} not found on device.")
        else:
            await read_characteristic(client, CHARACTERISTIC_UUID_PH, "pH Value")


# Run the main loop
asyncio.run(main())
