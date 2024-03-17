import logging
from app.adapters.agent_mqtt_adapter import AgentMQTTAdapter
from app.adapters.hub_http_adapter import HubHttpAdapter 
from app.adapters.hub_mqtt_adapter import HubMqttAdapter
from config import MQTT_TOPIC, HUB_MQTT_TOPIC  # Оскільки брокер та порт визначаються всередині класів

if __name__ == "__main__":
    # Configure logging settings
    logging.basicConfig(
        level=logging.INFO, 
        format="[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s",
        handlers=[
            logging.StreamHandler(),  # Output log messages to the console
            logging.FileHandler("app.log"),  # Save log messages to a file
        ],
    )

    # Create an instance of the HubMQTTAdapter using the configuration
    hub_adapter = HubMqttAdapter(topic=HUB_MQTT_TOPIC)

    # Create an instance of the AgentMQTTAdapter using the configuration
    agent_adapter = AgentMQTTAdapter(topic=MQTT_TOPIC)

    try:
        # Connect to the MQTT broker and start listening for messages
        agent_adapter.connect()
        agent_adapter.start()
        while True:
            pass
    except KeyboardInterrupt:
        # Stop the MQTT adapter and exit gracefully if interrupted by the user
        agent_adapter.stop()
        logging.info("System stopped.")
