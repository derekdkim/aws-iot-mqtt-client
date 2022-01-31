from geopy import distance


def calculate_distance(self, incoming):
    """
    Uses GeoPy to calculate distance
    then prints distance between object and incoming
    """
    # Use GeoPy haversine formula to calculate distance
    try:
        client_coord = (self.lat, self.lng)
        payload_coord = (incoming["lat"], incoming["lng"])
        print(
            f"Distance to {incoming['id']}: "
            f"{round(distance.distance(client_coord, payload_coord).km)}km"
        )
    except:
        print("Error: Failed to calculate distance with other client.")
