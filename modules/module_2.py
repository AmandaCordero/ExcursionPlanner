import simpy
import numpy as np
from ..utils.map_utils import Map
from defuzzification_module import compute_fuzzy_output

def simulate_excursion(map_data, weather, excursionists):
    env = simpy.Environment()

    # Configurar el entorno con los procesos iniciales
    setup(env)

    # Ejecutar la simulación
    env.run()

class Enviroment:
    def __init__(self, guide, excur, weather, path, env):
        self.guide = guide
        self.excur = excur
        self.weather = weather
        self.path = path
        self.mark = [""] * len(self.path)
        self.lunch = False
        self.env = env
        
    
    def get_time_of_day(self):
        return (env.now + 7) % 24
    
    def calculate_dispersion(self):
        firstexc = self.guide.current_position
        for exc in self.excur:
            if exc.current_position < firstexc:
                firstexc = exc.current_position
        return (self.guide.current_position - firstexc)/len(self.path)
        
class GuideAgent:
    def __init__(self, enviroment):
        self.name = "el guia"
        self.vel = np.random.uniform(2, 4)
        self.beliefs = {}
        self.desires = {}
        self.intentions = []
        self.enviroment = enviroment
        self.current_position = 0
        
    def move(self, point1, point2, env, ma):
        yield env.timeout(ma.size[point1]/self.vel)
        print(f"{self.name} llegó a {ma.points[point2]} en el tiempo {env.now}")
        self.current_position = point2
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
        self.beliefs["time_of_day"] = self.environment.get_time_of_day()
        self.beliefs["dispersion"] = self.environment.calculate_dispersion()

    def generate_desires(self):
        self.desires["keep_together"] = self.beliefs["time_of_day"] < 18
        self.desires["lunch"] = self.beliefs["time_of_day"] > 12 and not self.enviroment.lunch
        self.desires["camp"] = self.beliefs["time_of_day"] > 18

    def form_intentions(self):
        if self.desires["camp"]:
            self.intentions.append("setup_camp")
        if self.desires["lunch"]:
            self.intentions.append("have_lunch")
        if self.desires["keep_together"] and self.beliefs["dispersion"] > 1/5:
            self.intentions.append("regroup")
        if len(self.intentions) == 0:
            self.intentions.append("keep_walking")


class ExcursionAgent:
    def __init__(self, name):
        self.name = name
        self.vel = np.random.uniform(0.5,3)
        self.beliefs = {}
        self.desires = {
            'user_fauna': 0.7,
            'user_flora': 0.6,
            'user_isolation': 0.8,
            'user_challenge': 0.9,
            'user_history': 0.8,
            'user_rivers': 0.5
        }
        self.intentions = {}
        self.current_position = 0

    def move(self, point1, point2, env, ma):
        yield env.timeout(ma.size[point1]/self.vel)
        print(f"{self.name} llegó a {ma.points[point2]} en el tiempo {env.now}")
        self.current_position = point2
        if point2 != len(ma.points) -1:
            self.update_beliefs()
            self.form_intentions()
            #revisar camp lunch y regroup
            
            yield env.timeout(self.intentions["rest"])
            self.vel = self.vel * self.intentions["walk"]
            env.process(self.move(point2, point2 + 1, env,ma))
        
    
    def update_beliefs(self, point_c, edge_c):
        self.beliefs["point"] = {
            'point_history': 0.7,
            'point_rivers': 0.2,
            'point_flora': 0.8,
            'point_fauna': 0.9
        }
        self.beliefs["path"] = {
            'path_fauna': 0.5,
            'path_flora': 0.6,
            'path_isolation': 0.7,
            'path_challenge': 0.8
        }

    def form_intentions(self):
        self.intentions["walk"] = compute_fuzzy_output(context='walking_speed', **(self.beliefs["path"] + self.desires))
        self.intentions["rest"] = compute_fuzzy_output(context='waiting_time', **(self.beliefs["point"] + self.desires))
        

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