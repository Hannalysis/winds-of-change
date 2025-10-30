from scripts.etl.uk_lat_long_fetch import get_lat_lon_nominatim
from unittest.mock import patch, Mock

@patch('scripts.etl.uk_lat_long_fetch.requests.get')
def test_get_lat_lon_nominatim_success(mock_get):
    print(f"mock_get is: {mock_get}")
    
    # Mocking a successful API response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{
        'lat': '51.5074',
        'lon': '-0.1278'
    }]
    mock_get.return_value = mock_response

    lat, lon = get_lat_lon_nominatim("London, UK")
    assert lat == '51.5074'
    assert lon == '-0.1278'

    mock_get.assert_called_once()
    args, _ = mock_get.call_args
    assert "nominatim.openstreetmap.org" in args[0] 