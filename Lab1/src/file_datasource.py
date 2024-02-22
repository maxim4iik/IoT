from csv import reader
from datetime import datetime
from domain.aggregated_data import AggregatedData
from domain.accelerometer import Accelerometer
from domain.parking import Parking
from domain.gps import Gps

class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.accelerometer_data = []
        self.gps_data = []
        self.parking_filename = parking_filename
        self.parking_data = []

    def startReading(self):
    # Reading accelerometer data
        with open(self.accelerometer_filename, 'r') as file:
            csv_reader = reader(file)
            next(csv_reader, None)  # Skip the header
            for row in csv_reader:
                if len(row) >= 3:  # Check if row has at least 3 elements
                    try:
                        x = int(row[0])
                        y = int(row[1])
                        z = int(row[2])
                        self.accelerometer_data.append(Accelerometer(x=x, y=y, z=z))
                    except ValueError as e:
                        print(f"Error processing accelerometer data row: {row} - {e}")
                else:
                    print(f"Row does not have enough elements: {row}")

    # Reading GPS data
        with open(self.gps_filename, 'r') as file:
            csv_reader = reader(file)
            next(csv_reader, None)  # Skip the header
            for row in csv_reader:
                if len(row) >= 2:  # Check if row has at least 2 elements
                    try:
                        longtitude = float(row[0])
                        latitude = float(row[1])
                        self.gps_data.append(Gps(longtitude=longtitude, latitude=latitude))
                    except ValueError as e:
                        print(f"Error processing GPS data row: {row} - {e}")
                else:
                    print(f"Row does not have enough elements: {row}")
    
    def startReadingParking(self):
        with open(self.parking_filename, 'r') as file:
            csv_reader = reader(file)
            next(csv_reader, None)  # Skip the header
            for row in csv_reader:
                if len(row) >= 3: 
                    try:
                        empty_count = int(row[0])
                        # Assuming the GPS data is in columns 1 and 2
                        gps = Gps(longtitude=float(row[1]), latitude=float(row[2]))
                        self.parking_data.append(Parking(empty_count=empty_count, gps=gps))
                    except ValueError as e:
                        print(f"Error processing parking data row: {row} - {e}")


    def read(self) -> AggregatedData:
        if not self.accelerometer_data or not self.gps_data or not self.parking_data:
            raise ValueError("No data available to read. Ensure 'startReading' has been called.")

        if self.parking_data:  
            parking = self.parking_data.pop(0) 
        else:
            parking = Parking(empty_count=0, gps=Gps(longitude=0.0, latitude=0.0)) 

        if self.accelerometer_data:
            accelerometer = self.accelerometer_data.pop(0)
        else:
            accelerometer = None

        if self.gps_data:
            gps = self.gps_data.pop(0)
        else:
            gps = None

        return AggregatedData(accelerometer=accelerometer, gps=gps, parking=parking, time=datetime.now())

    def stopReading(self):
        self.accelerometer_data = []
        self.gps_data = []

