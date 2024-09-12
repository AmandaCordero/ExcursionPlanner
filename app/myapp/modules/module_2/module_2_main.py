import simpy
import numpy as np
# from ..utils.map_utils import Map
from .defuzzification_module import compute_fuzzy_output


def simulate_excursion(desires, route, map):
        
    # Configuración del entorno y ejecución de la simulación
    env = simpy.Environment()

    path = Path()
    # Ampliar la cantidad de puntos y tamaños en el camino
    path.points = route
    path.size = []  # Distancias entre los puntos
    for i in range(len(route)):
        if i == 0:
            continue
        my_tuple = (route[i-1], route[i])
        path.size.append(map.edges_size[my_tuple])

    # Crear más excursionistas para un caso más grande
    guide = GuideAgent(None)  # El entorno aún no se asigna
    excursion_agents = []

    for i in range(len(desires)):
       excursion_agents.append(ExcursionAgent(f'exc{i}', None,desires[i]))


    environment = Enviroment(guide, excursion_agents, path, env, map)

    # Asignar el entorno a los agentes
    guide.enviroment = environment
    for exc in excursion_agents:
        exc.enviroment = environment

    # print(path.size)
    # Ejecutar los procesos de movimiento
    env.process(guide.move(0, 1, env, path))
    for exc in excursion_agents:
        env.process(exc.move(0, 1, env, path))

    env.run()



class Enviroment:
    def __init__(self, guide, excur, path, env, map):
        self.guide = guide
        self.excur = excur
        self.path = path
        self.mark = [""] * len(self.path.points)
        self.had_lunch = False
        self.env = env
        self.regroup_count = 0  # Contador de excursionistas que llegaron al punto de reagrupación
        self.lunch_count = 0  # Contador de excursionistas que llegaron al almuerzo
        self.camp_count = 0   # Contador de excursionistas que llegaron al campamento
        self.map = map

    def get_time_of_day(self):
        return (self.env.now + 7) % 24
    
    def calculate_dispersion(self):
        firstexc = self.guide.current_position
        for exc in self.excur:
            if exc.current_position < firstexc:
                firstexc = exc.current_position
        return (self.guide.current_position - firstexc) / len(self.path.points)
    
    def regroup(self, point):
        # Verificar si todos los excursionistas han llegado al punto de reagrupación
        self.regroup_count += 1
        if self.regroup_count == len(self.excur)+1:
            log_trace(f"Todos los excursionistas han llegado al punto de reagrupación {point}.")
            self.regroup_count = 0  # Reiniciar el contador
            # Reanudar el movimiento de todos los excursionistas
            self.env.process(self.guide.move(point, point +1, self.env,self.path))
            for exc in self.excur:
                exc.reanudar(self.env, point, point + 1, self.path)
    
    def lunch(self, point):
        # Verificar si todos los excursionistas han llegado al punto de almuerzo
        self.lunch_count += 1
        if self.lunch_count == len(self.excur)+1:
            log_trace(f"Todos los excursionistas han llegado al punto de almuerzo {point}.")
            self.had_lunch = True
            self.lunch_count = 0  # Reiniciar el contador
            # Reanudar el movimiento de todos los excursionistas
            
            yield self.env.timeout(0.5)
            self.env.process(self.guide.move(point, point +1, self.env,self.path))
            for exc in self.excur:
                exc.reanudar(self.env, point, point + 1, self.path)
    
    def camp(self, point):
        # Verificar si todos los excursionistas han llegado al punto de campamento
        self.camp_count += 1
        if self.camp_count == len(self.excur) +1:
            log_trace(f"Todos los excursionistas han llegado al campamento en {point}.")
            self.camp_count = 0  # Reiniciar el contador
            # Reanudar el movimiento de todos los excursionistas
            
            yield self.env.timeout(10)
            self.had_lunch = False
            self.env.process(self.guide.move(point, point +1, self.env,self.path))
            for exc in self.excur:
                exc.reanudar(self.env, point, point + 1, self.path)


class GuideAgent:
    def __init__(self, enviroment):
        self.name = "el guia"
        self.vel = np.random.uniform(3, 4)
        self.beliefs = {}
        self.desires = {}
        self.intentions = []
        self.enviroment = enviroment
        self.current_position = 0
        
    def move(self, point1, point2, env, ma):
        yield env.timeout(ma.size[point1] / self.vel)
        log_trace(f"{self.name} llegó a {ma.points[point2]} en el tiempo {self.enviroment.get_time_of_day()}")
        self.current_position = point2
        if point2 != len(ma.points) - 1:
            self.intentions = []
            self.update_beliefs()
            self.generate_desires()
            self.form_intentions()
            if "keep_walking" in self.intentions:
                self.enviroment.mark[point2] = "continue"
                env.process(self.move(point2, point2 + 1, env, ma))
            elif "setup_camp" in self.intentions:
                self.enviroment.mark[point2] = "camp"
                env.process(self.enviroment.camp(point2))  # Lógica para acampar
            elif "have_lunch" in self.intentions:
                self.enviroment.mark[point2] = "lunch"
                env.process(self.enviroment.lunch(point2))  # Lógica para almorzar
            elif "regroup" in self.intentions:
                self.enviroment.mark[point2] = "regroup"
                self.enviroment.regroup(point2)  # Reagrupar

    def update_beliefs(self):
        self.beliefs["time_of_day"] = self.enviroment.get_time_of_day()
        self.beliefs["dispersion"] = self.enviroment.calculate_dispersion()

    def generate_desires(self):
        self.desires["keep_together"] = self.beliefs["time_of_day"] < 18
        self.desires["lunch"] = self.beliefs["time_of_day"] > 11 and not self.enviroment.had_lunch
        self.desires["camp"] = self.beliefs["time_of_day"] > 18

    def form_intentions(self):
        if self.desires["camp"]:
            self.intentions.append("setup_camp")
        if self.desires["lunch"]:
            self.intentions.append("have_lunch")
        if self.desires["keep_together"] and self.beliefs["dispersion"] > 1 / 5:
            self.intentions.append("regroup")
        if len(self.intentions) == 0:
            self.intentions.append("keep_walking")


class ExcursionAgent:
    def __init__(self, name, enviroment, desires):
        self.name = name
        self.vel = np.random.uniform(2, 3)
        self.beliefs = {}
        self.desires = {}
        self.desires["point"] = {
            'user_flora': desires[2],
            'user_fauna': desires[3],
            'user_history': desires[4],
            'user_rivers':desires[5]
        }
        self.desires["path"] = {
            'user_isolation': desires[0],
            'user_challenge':desires[1],
            'user_flora': desires[2],
            'user_fauna': desires[3]
        }
        
        self.intentions = {}
        self.current_position = 0
        self.enviroment = enviroment

    def move(self, point1, point2, env, ma):
        yield env.timeout(ma.size[point1] / self.vel)
        log_trace(f"{self.name} llegó a {ma.points[point2]} en el tiempo {self.enviroment.get_time_of_day()}")
        self.current_position = point2
        if point2 != len(ma.points) - 1:
            self.update_beliefs(self.enviroment.map.points[ma.points[point2]], self.enviroment.map.edges[(ma.points[point2], ma.points[point2+1])])
            self.form_intentions()
            
            if self.enviroment.mark[point2] == "regroup":
                self.enviroment.regroup(point2)
            elif self.enviroment.mark[point2] == "lunch":
                env.process(self.enviroment.lunch(point2))
            elif self.enviroment.mark[point2] == "camp":
                env.process(self.enviroment.camp(point2))
            else:
                # Si no es reagrupación, camp o almuerzo, continuar el movimiento normal
                yield env.timeout(self.intentions["rest"]/60)
                self.vel = self.vel * self.intentions["walk"]
                env.process(self.move(point2, point2 + 1, env, ma))

    def reanudar(self, env, point1, point2, ma):
        # Reanudar el movimiento después de reagruparse, almorzar o acampar
        log_trace(f"{self.name} reanuda el movimiento desde {ma.points[point1]} hacia {ma.points[point2]}.")
        env.process(self.move(point1, point2, env, ma))

    def update_beliefs(self, point_c, edge_c):
        self.beliefs["point"] = {
            'point_flora': point_c[2],
            'point_fauna':point_c[3],
            'point_history': point_c[4],
            'point_rivers': point_c[5]
        }
        self.beliefs["path"] = {
            'path_isolation': edge_c[0],
            'path_challenge':edge_c[1],
            'path_flora': edge_c[2],
            'path_fauna': edge_c[3]
        }

    def form_intentions(self):
        self.intentions["walk"] = compute_fuzzy_output(context='walking_speed', **(self.beliefs["path"] | self.desires["path"]))
        self.intentions["rest"] = compute_fuzzy_output(context='waiting_time', **(self.beliefs["point"] | self.desires["point"]))


class Path:
    def __init__(self):
        self.points = []
        self.size = []  

def log_trace(message):
    with open("./myapp/utils/trace.txt", "a") as log_file:
        log_file.write(message + "\n")