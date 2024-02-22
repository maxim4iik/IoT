from dataclasses import dataclass, field
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.parking import Parking

@dataclass
class AggregatedData:
    accelerometer: Accelerometer
    gps: Gps
    parking: Parking = field(default_factory=Parking)
    time: datetime = field(default_factory=datetime.now) 
