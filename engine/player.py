class Player:
    def __init__(self, name: str, color: str, controller = None):
        self.name = name
        self.color = color
        self.controller = controller
        self.owned_nodes = []