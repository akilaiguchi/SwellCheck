import requests

# TODO: this only changes time, doesn't move back date for pst. fix the code here later
def calculate_pst(utc: int) -> int:
    if utc < 8:
        return utc + 16
    else:
        return utc - 8


class BuoyScanner:

    # Initialize specific buoy
    def __init__(self, buoy_id: str):
        self.buoy_id = buoy_id
        self.url = f"https://www.ndbc.noaa.gov/data/realtime2/{self.buoy_id}.txt"
        response = requests.get(self.url)
        
        # Check if the response is successful
        if response.status_code == 404:
            raise ValueError(f'Buoy {self.buoy_id} not found')
        elif response.status_code != 200:
            raise RuntimeError(f"NDBC server returned an unexpected error: {response.status_code}")

        # Check if the response has at least 3 lines
        self.lines = response.text.split('\n')
        if len(self.lines) < 3:
            # throw exception;
            raise RuntimeError(f'Buoy has no recorded data')

        self.headers = self.lines[0].split()

        # TODO: optimize THIS
        # Parse all data lines (skip first 2 header lines)
        self.data = []
        for line in self.lines[2:]:
            if line.strip():  # Skip empty lines
                values = line.split()
                if len(values) == len(self.headers):
                    # Keep only columns 0-4, 8-11, 14
                    indices = [0, 1, 2, 3, 4, 8, 9, 10, 11, 14]
                    filtered_headers = [self.headers[i] for i in indices if i < len(self.headers)]
                    filtered_values = [values[i] for i in indices if i < len(values)]
                    self.data.append(dict(zip(filtered_headers, filtered_values)))
    
    # Get lates data of the buoy
    def getLatestData(self) -> str:
        latestData = f'''
            Latest wave information for buoy {self.buoy_id}:
            Date: {self.data[0]['MM']}/{self.data[0]['DD']}/{self.data[0]['#YY']}
            Time (UTC): {self.data[0]['hh']}:{self.data[0]['mm']}
            Time (PST): {calculate_pst(int(self.data[0]['hh']))}:{self.data[0]['mm']}


            Wave Height: {self.data[0]['WVHT']} m
            Dominant Period: {self.data[0]['DPD']} sec
            Average Period: {self.data[0]['APD']} sec
            Mean Wave Direction: {self.data[0]['MWD']} deg
            Water Temp: {self.data[0]['WTMP']}°C 
            '''
        return latestData

    def printLatestData(self) -> None:
        print(self.getLatestData())

    # TODO: add methods for last x days. last x weeks. last month.
        