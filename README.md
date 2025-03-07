# Geolocation Utility

## Overview
This utility provides geolocation information for cities and zip codes within the United States using the OpenWeatherMap Geocoding API.

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Installation
1. Clone the repository
2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
Run the utility from the command line:

```bash
python geoloc_util.py "Madison, WI" "12345" "Chicago, IL" "10001"
```

### Command-line Arguments
- Accepts multiple locations as arguments
- Supports city and state combinations (e.g., "Madison, WI")
- Supports US zip codes (e.g., "12345")

## Running Tests
To run the integration tests:
```bash
python -m pytest tests/
```

## API Key
The utility uses a provided OpenWeatherMap API key. For production use, replace the API key in the source code or use environment variables.

## Limitations
- Only supports locations within the United States
- Uses the first result when multiple locations are returned
- Requires an active internet connection
- Subject to OpenWeatherMap API rate limits

## Dependencies
- requests: HTTP library for API calls
- pytest: Testing framework
- argparse: Command-line argument parsing
