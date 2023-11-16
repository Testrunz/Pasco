# pasco_sensor.py
from pasco import PASCOBLEDevice
from influxdb_client import Point  # Import the Point class

class EventEmitter:
    def __init__(self):
            self.listeners = {}
    
    def on(self, event, listener):
        if event in self.listeners:
            self.listeners[event].append(listener)
        else:
            self.listeners[event] = [listener]   
    def emit(self, event, *args, **kwargs):
        if event in self.listeners:
            for listener in self.listeners[event]:
                listener(*args, **kwargs)

    def remove_listener(self, event, listener):
        if event in self.listeners:
            self.listeners[event].remove(listener)
            if len(self.listeners[event]) == 0:
                del self.listeners[event]

    def remove_all_listeners(self, event=None):
        if event:
            self.listeners.pop(event, None)
        else:
            self.listeners = {}
def temperature(temp, write_api,influx_bucket):
    point = Point("temperature").field("value", temp)
    write_api.write(bucket=influx_bucket, record=point)