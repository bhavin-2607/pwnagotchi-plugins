import paho.mqtt.client as mqtt
import requests
import json
from datetime import datetime
from pwnagotchi import plugins

class MacAddressLogger(plugins.Plugin):
    __author__ = 'pyRegex'
    __version__ = '1.2.0'
    __license__ = 'MIT'

    def __init__(self):
        super(MacAddressLogger, self).__init__()

        # Load plugin configuration
        self.mode = self.options.get("mode", "mqtt")  # Default to MQTT if not set

        if self.mode not in ["mqtt", "http"]:
            self.log.error('Invalid mode. Use "mqtt" or "http". Defaulting to "mqtt".')
            self.mode = "mqtt"

        # Load MQTT settings
        if self.mode == "mqtt":
            mqtt_config = self.options.get("mqtt", {})
            self.mqtt_broker = mqtt_config.get("broker", "mqtt.example.com")
            self.mqtt_port = mqtt_config.get("port", 1883)
            self.mqtt_username = mqtt_config.get("username", "your_username")
            self.mqtt_password = mqtt_config.get("password", "your_password")

            # Initialize MQTT client
            self.mqtt_client = mqtt.Client()
            self.mqtt_client.username_pw_set(self.mqtt_username, self.mqtt_password)
            try:
                self.mqtt_client.connect(self.mqtt_broker, self.mqtt_port, 60)
                self.log.info("Connected to MQTT broker with authentication.")
            except Exception as e:
                self.log.error(f"Failed to connect to MQTT broker: {e}")

        # Load HTTP settings
        elif self.mode == "http":
            http_config = self.options.get("http", {})
            self.http_url = http_config.get("url", "http://your-http-server.com/api")

    def on_loaded(self):
        self.log.info(f"MAC Address Logger Plugin loaded. Mode: {self.mode}")

    def on_handshake(self, agent, filename, access_point):
        mac_address = access_point.get('station', 'Unknown')  # Get MAC address safely
        self.log.info(f"Handshake captured from {mac_address}")

        if self.mode == "mqtt":
            self.publish_mqtt(mac_address, filename)
        elif self.mode == "http":
            self.send_http_request(mac_address, filename)

    def publish_mqtt(self, mac_address, filename):
        topic = f"pwnagotchi/handshake/{mac_address}"
        try:
            self.mqtt_client.publish(topic, filename)
            self.log.info(f"Handshake uploaded to MQTT broker: {topic}")
        except Exception as e:
            self.log.error(f"Failed to publish to MQTT broker: {e}")

    def send_http_request(self, mac_address, filename):
        headers = {'Content-Type': 'application/json'}
        data = {
            "deviceID": "0000260719990000",
            "deviceName": "ESP32 test",
            "timestamp": datetime.utcnow().isoformat() + "Z",  # Dynamic UTC timestamp
            "mac": mac_address,
            "handshake_file": filename
        }

        try:
            response = requests.post(self.http_url, headers=headers, json=data)
            if response.status_code == 200:
                self.log.info(f"Handshake sent to HTTP server successfully: {response.text}")
            else:
                self.log.error(f"Failed to send HTTP request: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            self.log.error(f"HTTP request failed: {e}")

    def on_unload(self):
        if self.mode == "mqtt":
            self.mqtt_client.disconnect()
            self.log.info("MQTT disconnected.")
        self.log.info("MAC Address Logger Plugin unloaded.")

# Instantiate the plugin
plugin = MacAddressLogger()
