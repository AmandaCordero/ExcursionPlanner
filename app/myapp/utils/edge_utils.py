class Edge:
    def __init__(self, id1, id2, distance, characteristics=None):
        self.id1 = id1
        self.id2 = id2
        self.distance = distance
        
        if characteristics is None:
            self.characteristics = {"morning":[0,0,0,0,0,0], "afternoon":[0,0,0,0,0,0], "night":[0,0,0,0,0,0]}
        else:
            self.characteristics = characteristics

        