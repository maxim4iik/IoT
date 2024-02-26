from datetime import datetime
from fastapi import FastAPI, WebSocketDisconnect, WebSocket, HTTPException
from pydantic import BaseModel, validator
from config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB
from sqlalchemy import Table, Column, Integer, String, Float, DateTime, create_engine, MetaData
import json
from typing import List, Set

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define the ProcessedAgentData table
processed_agent_data = Table(
    "processed_agent_data",metadata,
    Column("id", Integer, primary_key=True, index=True), 
    Column("road_state", String),
    Column("x", Float),
    Column("y", Float),
    Column("z", Float),
    Column("latitude", Float), 
    Column("longitude", Float), 
    Column("timestamp", DateTime),
)


# FastAPI models
class AccelerometerData(BaseModel): 
    x: float
    y: float
    z: float


class GpsData(BaseModel): 
    latitude: float
    longitude: float

class AgentData(BaseModel):
    accelerometer: AccelerometerData
    gps: GpsData
    timestamp: datetime

    @validator('timestamp') 
    def check_timestamp(cls, value):
        if not isinstance(value, datetime):
            raise ValueError("Timestamp must be a datetime object")
        return value


class  ProcessedAgentData(BaseModel):
    road_state: str
    agent_data: AgentData

class ProcessedAgentDataInDB(BaseModel):
    id: int
    road_state: str 
    x: float
    y: float 
    z: float
    latitude: float 
    longitude: float 
    timestamp: datetime


app = FastAPI()
subscriptions: Set[WebSocket] = set()
# FastAPI WebSocket endpoint
@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    subscriptions.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        subscriptions.remove(websocket)
# Function to send data to subscribed users
async def send_data_to_subscribers(data):
    for websocket in subscriptions:
        await websocket.send_json(data)



# FastAPI CRUDL endpoints
@app.post("/processed_agent_data/")
async def create_processed_agent_data(data: List[ProcessedAgentData]):
    # Insert data to database
    with engine.connect() as connection:
        for item in data:
            insert_stmt = processed_agent_data.insert().values(
                road_state=item.road_state,
                x=item.agent_data.accelerometer.x,
                y=item.agent_data.accelerometer.y,
                z=item.agent_data.accelerometer.z,
                latitude=item.agent_data.gps.latitude,
                longitude=item.agent_data.gps.longitude,
                timestamp=item.agent_data.timestamp
            )
            connection.execute(insert_stmt)
    # Send data to subscribers
    await send_data_to_subscribers(data)
    return {"status": "Data inserted successfully"}

@app.get("/processed_agent_data/{processed_agent_data_id}",response_model=ProcessedAgentDataInDB)
def  read_processed_agent_data(processed_agent_data_id: int): 
    # Get data by id
    with engine.connect() as connection:
        query = processed_agent_data.select()
        result = connection.execute(query)
        data = [
            ProcessedAgentDataInDB(
                id=row['id'],
                road_state=row['road_state'],
                x=row['x'],
                y=row['y'],
                z=row['z'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                timestamp=row['timestamp']
            )
            for row in result.fetchall()
        ]
    return data
    pass

@app.get("/processed_agent_data/", response_model=List[ProcessedAgentDataInDB])
def  list_processed_agent_data(): 
        # Get list of data
    with engine.connect() as connection:
        query = processed_agent_data.select()
        result = connection.execute(query)
        data = [
            ProcessedAgentDataInDB(
                id=row['id'],
                road_state=row['road_state'],
                x=row['x'],
                y=row['y'],
                z=row['z'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                timestamp=row['timestamp']
            )
            for row in result.fetchall()
        ]
    return data

@app.put("/processed_agent_data/{processed_agent_data_id}", response_model=ProcessedAgentDataInDB)
def  update_processed_agent_data( processed_agent_data_id: int,data: ProcessedAgentData ):
        # Update data
    pass

@app.delete("/processed_agent_data/{processed_agent_data_id}",response_model=ProcessedAgentDataInDB)
def  delete_processed_agent_data(processed_agent_data_id: int): 
    pass

if  __name__ == "__main__":
    import  uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


# server reload
# uvicorn main:app --reload

# Task 1 
# curl -X POST http://localhost:8000/processed_agent_data/ \
# -H "Content-Type: application/json" \
# -d '[{"road_state": "wet", "agent_data": {"accelerometer": {"x": 1.0, "y": 2.0, "z": 3.0}, "gps": {"latitude": 40.712776, "longitude": -74.005974}, "timestamp": "2024-02-26T12:00:00Z"}}]'

# Task 2
# curl http://localhost:8000/processed_agent_data/1
                        
# Task 3
# curl http://localhost:8000/processed_agent_data/
                        
# Task 4
# curl -X PUT http://localhost:8000/processed_agent_data/1 \
# -H "Content-Type: application/json" \
# -d '{"road_state": "сухо", "agent_data": {"accelerometer": {"x": 1.1, "y": 2.2, "z": 3.3}, "gps": {"latitude": 40.713776, "longitude": -74.006974}, "timestamp": "2024-02-27T12:00:00Z"}}'

# Task 5
# curl -X DELETE http://localhost:8000/processed_agent_data/1



