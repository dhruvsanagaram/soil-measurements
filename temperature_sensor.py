import asyncio
from bleak import BleakClient, BleakScanner

# Replace with your ESP32's BLE service and characteristic UUIDs
SERVICE_UUID = "12345678-1234-1234-1234-1234567890ab"
CHARACTERISTIC_UUID = "87654321-4321-4321-4321-0987654321ba"
DEVICE_NAME = "ESP32_SPIFFS_BLE_Server"  # Name of your ESP32 BLE device

async def main():
    # Scan for the BLE device
    print("Scanning for devices...")
    devices = await BleakScanner.discover()
    esp32_device = None

    for device in devices:
        # Check if device.name is not None to avoid TypeError
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

        # Check if the service UUID is present
        services = await client.get_services()
        if SERVICE_UUID not in [service.uuid for service in services]:
            print(f"Service UUID {SERVICE_UUID} not found on device.")
            return

        # Read data from the characteristic
        try:
            data = await client.read_gatt_char(CHARACTERISTIC_UUID)
            if data:
                print("Data from ESP32 SPIFFS:")
                print(data.decode('utf-8'))
            else:
                print("Received data is empty.")
        except Exception as e:
            print(f"Failed to read data: {e}")
            
# Run the main loop
asyncio.run(main())
