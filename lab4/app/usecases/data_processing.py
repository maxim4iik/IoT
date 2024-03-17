from datetime import datetime
from pydantic import BaseModel, Field

# Assuming these classes are defined in respective files
from app.entities.agent_data import AgentData, AccelerometerData, GpsData
from app.entities.processed_agent_data import ProcessedAgentData

def classify_road_condition(z: float) -> str:
    # Define threshold for simplicity, this should be based on empirical data
    threshold = 0.5  # This is a made-up threshold for demonstration
    if abs(z) < threshold:
        return "smooth"
    else:
        return "rough"

def process_agent_data(agent_data: AgentData) -> ProcessedAgentData:
    """
    Process agent data and classify the state of the road surface.
    Parameters:
        agent_data (AgentData): Agent data that contains accelerometer, GPS, and timestamp.
    Returns:
        processed_data (ProcessedAgentData): Processed data containing the classified state of the road surface and agent data.
    """
    # Classify the road condition based on the z-coordinate of accelerometer data
    road_state = classify_road_condition(agent_data.accelerometer.z)
    
    # Create the ProcessedAgentData instance
    processed_data = ProcessedAgentData(
        road_state=road_state,
        agent_data=agent_data
    )
    
    return processed_data
