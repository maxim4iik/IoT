import paho.mqtt.client as mqtt
from app.entities.agent_data import AgentData
from app.usecases.data_processing import process_agent_data
import os

class AgentMQTTAdapter:
    def __init__(self, topic):
        self.broker_host = os.getenv('MQTT_BROKER_HOST', 'mqtt') 
        self.broker_port = int(os.getenv('MQTT_BROKER_PORT', 1883))  
        self.topic = topic
        self.client = mqtt.Client()

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        print(f"Message received: {msg.topic} {msg.payload}")
        # Тут ви маєте обробити повідомлення

    def connect(self):
        try:
            self.client.connect(self.broker_host, self.broker_port, 60)
        except Exception as e:
            print(f"Could not connect to MQTT Broker: {e}")

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
