import os
import json
from utilities.State import State
from typing import Any,Dict, List, Tuple  # For type hints

class RouteData:
    def __init__(self, json_string):
        self.data = json.loads(json_string)  # Assign data to self.data
        self.segments = self.data.get("segments", [])  # Extract segments from self.data
        self.intersections = {i["identifier"]: i for i in self.data.get("intersections", [])}  # Map for fast lookup

    def get_address(self) -> str:
        return self.data.get("address", "No Address")

    def get_distance(self) -> int:
        return self.data.get("distance", 0)

    def get_initial_final(self) -> Dict[str, int]:
        return {"initial": self.data.get("initial", 0), "final": self.data.get("final", 0)}

    def get_intersections(self) -> List[Dict[str, Any]]:
        return list(self.intersections.values())

    def get_segments(self, state_id):
        """Fetch segments originating from the given state_id."""
        return [segment for segment in self.segments if segment["origin"] == state_id]

    def get_state(self, state_id):
        """Fetch a State object for a given state_id using intersection data."""
        intersection = self.intersections.get(state_id)
        if intersection:
            return State(id=state_id, latitude=intersection["latitude"], longitude=intersection["longitude"])
        else:
            raise ValueError(f"No intersection data found for state ID: {state_id}")

