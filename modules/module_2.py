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
        self.mark = [""] * len(self.path)
        self.lunch = False
        
        def get_current_position(self, agent):
            pass
        
        def get_time_of_day(self):
            pass
        
        def calculate_dispersion(self):
            pass
        
class GuideAgent:
    def __init__(self, enviroment):
        self.name = "el guia"
        self.vel = np.random.uniform(2, 4)
        self.beliefs = {}
        self.desires = {}
        self.intentions = []
        self.enviroment = enviroment
        
    def move(self, point1, point2, env, ma):
        yield env.timeout(ma.size[point1]/self.vel)
        print(f"{self.name} llegó a {ma.points[point2]} en el tiempo {env.now}")
        if point2 != len(ma.points) -1:
            self.intentions = []
            self.update_beliefs()
            self.generate_desires()
            self.form_intentions()
            if "keep_walking" in self.intentions:
                self.enviroment.mark[point2] = "continue"
                env.process(self.move(point2, point2 + 1, env,ma)) ########
            elif "setup_camp" in self.intentions:
                self.enviroment.mark[point2] = "camp"
            elif "lunch" in self.intentions:
                self.enviroment.mark[point2] = "lunch"
            elif "regroup" in self.intentions:
                self.enviroment.mark[point2] = "regroup"
            
    
    def update_beliefs(self):
        self.beliefs["current_position"] = environment.get_current_position(self)
        self.beliefs["time_of_day"] = environment.get_time_of_day()
        self.beliefs["dispersion"] = environment.calculate_dispersion()

    def generate_desires(self):
        self.desires["keep_together"] = self.beliefs["time_of_day"] < 18
        self.desires["lunch"] = self.beliefs["time_of_day"] > 12 and not self.enviroment.lunch
        self.desires["camp"] = self.beliefs["time_of_day"] > 18

    def form_intentions(self):
        if self.desires["camp"]:
            self.intentions.append("setup_camp")
        if self.desires["lunch"]:
            self.intentions.append("have_lunch")
        if self.desires["keep_together"] and self.beliefs["dispersion"] > 5:
            self.intentions.append("regroup")
        if len(self.intentions) == 0:
            self.intentions.append("keep_walking")


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