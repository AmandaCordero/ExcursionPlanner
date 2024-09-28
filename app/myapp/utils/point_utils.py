class Point:
    def __init__(self, id, location, height, characteristics=None):
        self.id = id
        self.height = height
        self.location = location
        
        if characteristics is None:
            self.characteristics = {"morning":[0,0,0,0,0,0], "afternoon":[0,0,0,0,0,0], "night":[0,0,0,0,0,0]}
        else:
            self.characteristics = characteristics