#!/usr/bin/env python3
import argparse
import requests
import sys
import re

class GeolocationUtility:
    API_KEY = 'f897a99d971b5eef57be6fafa0d83239'
    BASE_URL = 'http://api.openweathermap.org/geo/1.0'

    @classmethod
    def parse_location(cls, location):
        """
        Parse location input into city, state, or zip code
        """
        # Remove any leading/trailing whitespace
        location = location.strip()
        
        # Check if it's a zip code (5 digits)
        if re.match(r'^\d{5}$', location):
            return {'type': 'zip', 'query': location}
        
        # Check for city, state format
        match = re.match(r'^([\w\s]+),\s*([A-Z]{2})$', location)
        if match:
            return {
                'type': 'city',
                'city': match.group(1).strip(),
                'state': match.group(2).strip()
            }
        
        raise ValueError(f"Invalid location format: {location}")

    @classmethod
    def get_location_coordinates(cls, location):
        """
        Fetch coordinates for a given location
        """
        try:
            parsed_location = cls.parse_location(location)
        except ValueError as e:
            print(f"Error parsing location: {e}", file=sys.stderr)
            return None

        try:
            if parsed_location['type'] == 'zip':
                # Coordinates by zip code endpoint
                response = requests.get(
                    f'{cls.BASE_URL}/zip',
                    params={
                        'zip': f"{parsed_location['query']},US",
                        'appid': cls.API_KEY
                    }
                )
            else:
                # Coordinates by city name endpoint
                response = requests.get(
                    f'{cls.BASE_URL}/direct',
                    params={
                        'q': f"{parsed_location['city']},{parsed_location['state']},US",
                        'limit': 1,
                        'appid': cls.API_KEY
                    }
                )
            
            response.raise_for_status()
            data = response.json()

            # Different response structure for zip vs city
            if parsed_location['type'] == 'zip':
                return {
                    'name': data.get('name', 'Unknown'),
                    'lat': data.get('lat'),
                    'lon': data.get('lon'),
                    'country': data.get('country')
                }
            else:
                # Take first result if available
                if data:
                    location_data = data[0]
                    return {
                        'name': location_data.get('name', 'Unknown'),
                        'state': parsed_location['state'],
                        'lat': location_data.get('lat'),
                        'lon': location_data.get('lon'),
                        'country': location_data.get('country')
                    }
                
            return None

        except requests.RequestException as e:
            print(f"API request error: {e}", file=sys.stderr)
            return None

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Fetch geolocation coordinates for given locations'
    )
    parser.add_argument(
        'locations', 
        nargs='+', 
        help='List of locations (city, state or zip code)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Process each location
    for location in args.locations:
        result = GeolocationUtility.get_location_coordinates(location)
        
        if result:
            print(f"Location: {location}")
            for key, value in result.items():
                print(f"{key.capitalize()}: {value}")
            print()  # Empty line between locations
        else:
            print(f"Could not retrieve coordinates for: {location}", file=sys.stderr)

if __name__ == '__main__':
    main()
