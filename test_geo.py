from util.geolocation import calculate_distance

zero_int_payload = {
  "lat": 0,
  "lng": 0,
  "id": "Equator"
}

string_payload = {
  "lat": "43.6532",
  "lng": "-79.3832",
  "id": "YYG"
}

invalid_payload = {
  "lat": "43.6532",
  "lng": "-79.3832",
  # "id": "YYG"
}

float_payload = {
  "lat": 43.6532,
  "lng": -79.3832,
  "id": "YYG"
}

class client_object:
    def __init__(self):
        self.lat = "49.2827"
        self.lng = "-123.1207"
    def onMessage(self, payload):
      # Mock onMessage
      calculate_distance(self, payload)

def test_calculate_distance_float_payload(capsys):
    """
    Test case for successful distance calculation from Vancouver to Toronto
    Takes payload lat lng with float data type
    """
    client_object().onMessage(float_payload)
    captured = capsys.readouterr()
    print(captured.out)
    assert captured.out == "Distance to YYG: 3368km\n"

def test_calculate_distance_string_payload(capsys):
    """
    Test case for successful distance calculation from Vancouver to Toronto
    Takes payload lat lng with string data type
    """
    client_object().onMessage(float_payload)
    captured = capsys.readouterr()
    print(captured.out)
    assert captured.out == "Distance to YYG: 3368km\n"

def test_calculate_distance_zero_int_payload(capsys):
    """
    Test case for successful distance calculation from Vancouver to Toronto
    Takes payload lat lng with string data type
    """
    client_object().onMessage(zero_int_payload)
    captured = capsys.readouterr()
    print(captured.out)
    assert captured.out == "Distance to Equator: 12337km\n"

def test_fail_calculate_distance(capsys):
    """Test case for failed distance calculation from Vancouver to Toronto"""
    client_object().onMessage(invalid_payload)
    captured = capsys.readouterr()
    print(captured.out)
    assert captured.out == "Error: Failed to calculate distance with other client.\n"
