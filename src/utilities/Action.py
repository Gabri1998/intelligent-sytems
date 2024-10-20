

class Action:
    def __init__(self, name, cost=1):
        self.name = name
        self.cost = cost

    def __repr__(self):
        return f"Action({self.name}, cost={self.cost})"
