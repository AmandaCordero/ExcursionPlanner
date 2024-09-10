import simpy
import numpy as np
from ..utils.map_utils import Map

def simulate_excursion(map_data, weather, excursionists):
    env = simpy.Environment()

    # Configurar el entorno con los procesos iniciales
    setup(env)

    # Ejecutar la simulación
    env.run()

class Enviroment:
    def __init__(self, guide, excur, weather, path):
        self.guide = guide
        self.excur = excur
        self.weather = weather
        self.path = path
        
class GuideAgent:
    def __init__(self):
        self.name = "el guia"
        self.vel = np.random.uniform(2, 4)
        
    def move(self, point1, point2, env, ma):
        yield env.timeout(ma.size[point1]/self.vel)
        print(f"{self.name} llegó a {ma.points[point2]} en el tiempo {env.now}")
        if point2 != len(ma.points) -1:
            env.process(self.move(point2, point2 + 1, env,ma))
    
    def perceive(self,enviroment):
        pass

class ExcursionAgent:
    def __init__(self, name):
        self.name = name
        self.vel = np.random.uniform(0.5,3)
        self.beliefs = {}
        self.desires = {}
        self.intentions = {}

    def move(self, point1, point2, env, ma):
        yield env.timeout(ma.size[point1]/self.vel)
        print(f"{self.name} llegó a {ma.points[point2]} en el tiempo {env.now}")
        if point2 != len(ma.points) -1:
            env.process(self.move(point2, point2 + 1, env,ma))
        
    
    def update_beliefs(self, environment):
        pass

    def generate_desires(self):
        pass

    def form_intentions(self):
        pass

    def act(self, environment):
        pass
    
class Path:
    def __init__(self):
        self.points = []
        self.size = []  
        self.slope = []  

env = simpy.Environment()

guide = GuideAgent()

ex1 = ExcursionAgent("exc1")
ex2 = ExcursionAgent("exc2")
ex3 = ExcursionAgent("exc3")
ex4 = ExcursionAgent("exc4")
ex5 = ExcursionAgent("exc5")

path = Path()
path.points = ['A', 'B', 'C']
path.size = [10,10]
path.slope = [0.5, -0.5]

env.process(guide.move(0, 1, env, path))
env.process(ex1.move(0, 1, env, path))
env.process(ex2.move(0, 1, env, path))
env.process(ex3.move(0, 1, env, path))
env.process(ex4.move(0, 1, env, path))
env.process(ex5.move(0, 1, env, path))

env.run()