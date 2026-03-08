# mqtt_client.py
"""
Handles all MQTT communication for the simulation.
Connects to the broker and publishes vehicle data.
"""

import paho.mqtt.client as mqtt
import threading
import json
import time
from config import *

class MQTTClient:
    def __init__(self):
        """
        Initializes the MQTT client.
        """
        self.client = mqtt.Client(client_id=MQTT_CLIENT_ID, protocol=mqtt.MQTTv311, transport="tcp")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.is_connected = False
        self.thread = threading.Thread(target=self.run, daemon=True)

    def on_connect(self, client, userdata, flags, rc):
        """
        Callback for when the client connects to the broker.
        """
        if rc == 0:
            print("MQTT: Connected to broker successfully.")
            self.is_connected = True
            # Subscribe to topics upon connection
            self.client.subscribe(MQTT_TOPIC_SPEED_CONTROL)
        else:
            print(f"MQTT: Failed to connect, return code {rc}\\n")

    def on_message(self, client, userdata, msg):
        """
        Callback for when a message is received from the broker.
        """
        print(f"MQTT: Received message on topic {msg.topic}: {msg.payload.decode()}")
        # Here you could add logic to handle incoming commands, e.g., from a separate dashboard
        pass

    def publish(self, topic, payload):
        """
        Publishes a message to a given MQTT topic.
        :param topic: The topic to publish to.
        :param payload: The data to send (will be converted to JSON).
        """
        if self.is_connected:
            json_payload = json.dumps(payload)
            self.client.publish(topic, json_payload)
        else:
            print("MQTT: Cannot publish, not connected.")

    def run(self):
        """
        Connects to the broker and starts the client loop.
        This should be run in a separate thread.
        """
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
            self.client.loop_forever()
        except Exception as e:
            print(f"MQTT: Error in client loop - {e}")
    
    def start(self):
        """
        Starts the MQTT client thread.
        """
        print("MQTT: Starting client thread...")
        self.thread.start()

    def stop(self):
        """
        Stops the MQTT client.
        """
        if self.is_connected:
            print("MQTT: Disconnecting from broker...")
            self.client.loop_stop()
            self.client.disconnect()
        self.is_connected = False

