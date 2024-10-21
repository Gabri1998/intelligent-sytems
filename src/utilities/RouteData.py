import os
import json

from typing import Any,Dict, List, Tuple  # For type hints


class RouteData:
    """Class to handle route data from JSON."""

    def __init__(self, json_string: str):
        self.data = json.loads(json_string)

    def get_address(self) -> str:
        return self.data.get("address", "No Address")

    def get_distance(self) -> int:
        return self.data.get("distance", 0)

    def get_initial_final(self) -> Dict[str, int]:
        return {"initial": self.data.get("initial", 0), "final": self.data.get("final", 0)}

    def get_intersections(self) -> List[Dict[str, Any]]:
        return self.data.get("intersections", [])

    def get_segments(self) -> List[Dict[str, Any]]:
        return self.data.get("segments", [])
