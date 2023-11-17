'''
geocoder if needed

'''
import json
import os
from geopy.geocoders import OpenCage, ArcGIS
from geopy.extra.rate_limiter import RateLimiter
from dotenv import load_dotenv

load_dotenv()

class Geocoder:
    def __init__(self, opencage_api_key):
        self.geolocator_nominatim = ArcGIS()
        self.geolocator_opencage = OpenCage(opencage_api_key)
        self.geocode_nominatim = RateLimiter(self.geolocator_nominatim.geocode, min_delay_seconds=1)
        self.geocode_opencage = RateLimiter(self.geolocator_opencage.geocode, min_delay_seconds=1)
        
    def geocode_address(self, address):
        location = self.geocode_nominatim(address)
        if location:
            return location.latitude, location.longitude
        else:
            print(f"ArcGIS could not find: {address}, trying OpenCage...")
            location = self.geocode_opencage(address)
            if location:
                return location.latitude, location.longitude
        return None, None

def main(): 
    geocoder = Geocoder(os.getenv('OPENCAGE_API_KEY'))
    with open('vegastestoffers.json', 'r') as file:
        data = json.load(file)
    
    for key, value in data.items():
        address = f"{value['street_address']} {value['city']} {value['state']} {value['zip']}"
        lat, lon = geocoder.geocode_address(address)
        if lat and lon:
            value['latitude'] = lat
            value['longitude'] = lon
        else:
            print(f"Could not geocode address: {address}")
    
    with open('updated_vegastestoffers.json', 'w') as file:
        json.dump(data, file, indent=4)

    return True

if __name__ == "__main__":
    main()
