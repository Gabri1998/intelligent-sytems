class State:
    def __init__(self, id, latitude=None, longitude=None):
        """
        Initialize a state with an identifier and optional latitude and longitude.
        
        Args:
            id (int): Unique identifier for the state.
            latitude (float): Latitude coordinate.
            longitude (float): Longitude coordinate.
        """
        self.id = id
        self.latitude = latitude
        self.longitude = longitude

    def __eq__(self, other):
        """Equality check based on state ID."""
        return self.id == other.id

    def __hash__(self):
        """Hash based on state ID for use in sets and dictionaries."""
        return hash(self.id)

    def __repr__(self):
        """String representation for debugging."""
        return f"State({self.id}, lat={self.latitude}, lon={self.longitude})"
