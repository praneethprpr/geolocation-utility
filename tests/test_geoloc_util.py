import pytest
import subprocess
import sys
import json

class TestGeolocationUtility:
    def test_city_state_location(self):
        """
        Integration test for city and state location
        """
        # Run the script as a subprocess
        result = subprocess.run(
            [sys.executable, 'geoloc_util.py', 'Madison, WI'], 
            capture_output=True, 
            text=True
        )
        
        # Check successful execution
        assert result.returncode == 0, f"Script failed: {result.stderr}"
        
        # Check output contains expected information
        output = result.stdout
        assert 'Location: Madison, WI' in output
        assert 'Name:' in output
        assert 'Lat:' in output
        assert 'Lon:' in output
        assert 'State: WI' in output

    def test_zip_code_location(self):
        """
        Integration test for zip code location
        """
        # Run the script as a subprocess
        result = subprocess.run(
            [sys.executable, 'geoloc_util.py', '12345'], 
            capture_output=True, 
            text=True
        )
        
        # Check successful execution
        assert result.returncode == 0, f"Script failed: {result.stderr}"
        
        # Check output contains expected information
        output = result.stdout
        assert 'Location: 12345' in output
        assert 'Name:' in output
        assert 'Lat:' in output
        assert 'Lon:' in output
        assert 'Country:' in output

    def test_multiple_locations(self):
        """
        Integration test for multiple locations
        """
        # Run the script as a subprocess
        result = subprocess.run(
            [sys.executable, 'geoloc_util.py', 'Madison, WI', '12345', 'Chicago, IL'], 
            capture_output=True, 
            text=True
        )
        
        # Check successful execution
        assert result.returncode == 0, f"Script failed: {result.stderr}"
        
        # Check output for multiple locations
        output = result.stdout
        assert 'Location: Madison, WI' in output
        assert 'Location: 12345' in output
        assert 'Location: Chicago, IL' in output

    def test_invalid_location(self):
        """
        Integration test for invalid location input
        """
        # Run the script as a subprocess
        result = subprocess.run(
            [sys.executable, 'geoloc_util.py', 'Invalid Location'], 
            capture_output=True, 
            text=True
        )
        
        # Check for error handling
        assert result.returncode == 0  # Should exit cleanly
        assert 'Error parsing location:' in result.stderr
