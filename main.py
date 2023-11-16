from pasco_sensor import PASCOBLEDevice, EventEmitter, temperature
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import certifi  # Import the certifi package


# InfluxDB connection details
influx_url = "https://us-east-1-1.aws.cloud2.influxdata.com"
influx_token = "4x0FzQ_ONfb1ecnq_9wR_Nda0ITZfLsUsqb6_wh6TJ1zkxaEw8iJ0zCaGFWvmLWBdT52Ha2LnD8jCwzWzoctwA=="
influx_org = "Learny"
influx_bucket = "temperature"

# Set the SSL certificate authority file to use certifi's certificates
ssl_ca_cert = certifi.where()

my_sensor = PASCOBLEDevice()
found_devices = my_sensor.scan()

# Initialize the InfluxDB client with the ssl_ca_cert parameter
influx_client = InfluxDBClient(
    url=influx_url,
    token=influx_token,
    org=influx_org,
    ssl_ca_cert=ssl_ca_cert  # Use certifi's certificates
)

print("\nDevices Found")
for i, ble_device in enumerate(found_devices):
    display_name = ble_device.name.split(">")
    print(f"{i}: {display_name}")

# Auto connect if only one sensor found
selected_device = input("Select a device: ") if len(found_devices) > 1 else 0

ble_device = found_devices[int(selected_device)]
my_sensor.connect(ble_device)

emitter = EventEmitter()
emitter.on("temperature", temperature)

# Initialize the InfluxDB client
influx_client = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

# Loop that will read/display the data and store it in InfluxDB
# for i in range(100):
while True:
    current_temp = my_sensor.read_data("Temperature")
    emitter.emit("temperature", current_temp, write_api, influx_bucket)
    print(f"Temperature {i + 1}: {current_temp}")

# Disconnect from the Pasco sensor
my_sensor.disconnect()

# Close the InfluxDB client connection
influx_client.close()