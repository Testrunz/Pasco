import tkinter as tk
from tkinter import ttk
from pasco.code_node_device import CodeNodeDevice
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import threading

# InfluxDB connection details
influx_url = "https://us-east-1-1.aws.cloud2.influxdata.com"
influx_token = "jIxIAM6M1ENnCdS3DD22G3uV2-w5MoputRR9dcA6LMdA3Ni2viA_3m_Gt4hduYGzVF_u5e6XlXS-mnkZfkkj_Q=="
influx_org = "Learny"
influx_bucket = "my-bucket"

code_node = CodeNodeDevice()
influx_client = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

data_point = Point("sensor_data").tag("device", "code_node")

# Create a variable to keep track of the running thread
data_thread = None

def addMenu(root):
    menubar = tk.Menu(root)
    fileMenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=fileMenu)
    fileMenu.add_command(label="EXIT", command=root.destroy)
    root.config(menu=menubar)

def readingData(flag, channel_name, data_point, write_api):
    try:
        while flag:
            channel_value = code_node.read_data(channel_name)
            data_point.field(channel_name, channel_value)
            write_api.write(bucket=influx_bucket, record=data_point)
            print(f"{channel_name} {channel_value}")
    except Exception as e:
        print(f"You have been closed the server!")
        
def start_action(device_entry, channel_entries):
    global data_thread  # Declare the thread as global
    device_id = device_entry.get()
    code_node.connect_by_id(device_id)

    for i, channel_entry in enumerate(channel_entries):
        channel_name = channel_entry.get()
        if channel_name:
            # Start a new thread for each channel
            data_thread = threading.Thread(target=readingData, args=(True, channel_name, data_point, write_api))
            data_thread.daemon = True
            data_thread.start()

def stop_action():
    code_node.disconnect()
    global data_thread  # Declare the thread as global
    if data_thread:
        data_thread.join()  # Wait for the thread to finish

def create_interface(root):
    device_label = tk.Label(root, text="Device ID:")
    device_label.pack()

    device_entry = tk.Entry(root)
    device_entry.pack()

    channels_label = tk.Label(root, text="Number of Channels:")
    channels_label.pack()

    num_channels = tk.IntVar()
    channels_selector = ttk.Combobox(root, textvariable=num_channels)
    channels_selector['values'] = [i for i in range(1, 5)]
    channels_selector.pack()

    channel_entries = []
    for i in range(4):
        channel_label = tk.Label(root, text=f"Channel {i + 1} Name:")
        channel_label.pack()
        channel_entry = tk.Entry(root)
        channel_entry.pack()
        channel_entries.append(channel_entry)

    start_button = tk.Button(root, text="Start", command=lambda: start_action(device_entry, channel_entries))
    start_button.pack()

    stop_button = tk.Button(root, text="Stop", command=stop_action)
    stop_button.pack()

    def update_channel_entries(*args):
        num = num_channels.get()
        for i, entry in enumerate(channel_entries):
            if i < num:
                entry.config(state='normal')
                channel_label.config(state='normal')
            else:
                entry.delete(0, tk.END)
                entry.config(state='disabled')
                channel_label.config(state='disabled')

    num_channels.trace('w', update_channel_entries)
    update_channel_entries()

root = tk.Tk()
root.title("Testrunz Asset Connector")
root.geometry("800x600+50+20")

addMenu(root)
create_interface(root)

def applicationSupportsSecureRestorableState(_):
    return True

root.mainloop()