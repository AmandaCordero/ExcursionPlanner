import simpy
import numpy as np
from .defuzzification_module import compute_fuzzy_output
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Simulation:

    def __init__(self):
        self.camp_points = []
        self.reagroup_points = []
        self.launch_points = []
        self.cost = 0
        self.verbose = False

    def simulate_excursion(self, desires, route, map, precomputed_data, verbose,simulation_data):

        self.cost = 0
        self.verbose = verbose

        self.camp_points = []
        self.reagroup_points = []
        self.launch_points = []
        
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

        rules = []
        for rule in simulation_data["rules"]:
            rules.append(Rule(rule["beliefset"], rule["desireset"]))

        dis = []
        for di in simulation_data["DI"]:
            dis.append(DI(di["priority"], di["desires"], di["intention"]))

        # Crear más excursionistas para un caso más grande
        guide = GuideAgent(None, self,rules, dis)  # El entorno aún no se asigna
        excursion_agents = []

        for i in range(len(desires)):
            excursion_agents.append(ExcursionAgent(f'exc{i}', None, desires[i], precomputed_data[i], self))


        environment = Enviroment(guide, excursion_agents, path, env, map, verbose,simulation_data["time"])

        # Asignar el entorno a los agentes
        guide.enviroment = environment
        for exc in excursion_agents:
            exc.enviroment = environment

        env.process(guide.move(1, 2, env, path))
        for exc in excursion_agents:
            env.process(exc.move(1, 2, env, path))

        env.run()

        return self.camp_points, self.reagroup_points, self.launch_points, self.cost


class Enviroment:
    def __init__(self, guide, excur, path, env, map, verbose, time):
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
        self.verbose = verbose
        self.time = time

    def get_time_of_day(self):
        return round((self.env.now + 7) % 24, 2)
    
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
            
            if self.verbose:
                print(f"Todos los excursionistas han llegado al punto de reagrupación {point}.")

            self.regroup_count = 0  # Reiniciar el contador
            # Reanudar el movimiento de todos los excursionistas
            yield self.env.timeout(self.time["regroup"])
            self.env.process(self.guide.move(point, point +1, self.env,self.path))
            for exc in self.excur:
                exc.reanudar(self.env, point, point + 1, self.path)
    
    def lunch(self, point):
        # Verificar si todos los excursionistas han llegado al punto de almuerzo
        self.lunch_count += 1
        if self.lunch_count == len(self.excur)+1:
            
            if self.verbose:
                print(f"Todos los excursionistas han llegado al punto de almuerzo {point}.")

            self.had_lunch = True
            self.lunch_count = 0  # Reiniciar el contador
            # Reanudar el movimiento de todos los excursionistas
            
            yield self.env.timeout(self.time["lunch"])
            self.env.process(self.guide.move(point, point +1, self.env,self.path))
            for exc in self.excur:
                exc.reanudar(self.env, point, point + 1, self.path)
    
    def camp(self, point):
        # Verificar si todos los excursionistas han llegado al punto de campamento
        self.camp_count += 1
        if self.camp_count == len(self.excur) +1:
            
            if self.verbose:
                print(f"Todos los excursionistas han llegado al campamento en {point}.")

            self.camp_count = 0  # Reiniciar el contador
            # Reanudar el movimiento de todos los excursionistas
            
            yield self.env.timeout(self.time["camp"])
            self.had_lunch = False
            self.env.process(self.guide.move(point, point +1, self.env,self.path))
            for exc in self.excur:
                exc.reanudar(self.env, point, point + 1, self.path)

class Rule:
    def __init__(self, beliefset = None, desireset = None):
        self.beliefset = beliefset if beliefset else []
        self.desireset = desireset if desireset else []

    def evaluate(self, beliefs):
        for b in self.beliefset:
            if beliefs[b[0]] < b[1]:
                return False
        return True
  
class DI:
    def __init__(self, priority, desires, intention):
        self.priority = priority
        self.desires = desires
        self.intention = intention
    

class GuideAgent:
    def __init__(self, enviroment, simulation, rules = None, dis = None):
        self.name = "el guia"
        self.beliefs = {}
        self.desires = {
            "keep_together": False,
            "lunch": False,
            "camp": False
        }
        self.intention = ""
        self.enviroment = enviroment
        self.current_position = 0
        self.simulation = simulation
        self.rules = rules if rules else None
        self.dis = dis if dis else None
        
    def move(self, point1, point2, env, ma):
        # Calcular quién es el excursionista más adelantado y su tiempo estimado de llegada
        fastest_time = None
        for exc in self.enviroment.excur:
            time_to_next_point = ma.size[point1] / exc.vel
            if fastest_time is None or time_to_next_point < fastest_time:
                fastest_time = time_to_next_point

        # El guía debe llegar un segundo antes que el más adelantado
        guide_time = max(0, fastest_time - 1 / 60)  # Evitar tiempos negativos

        # Esperar el tiempo ajustado
        yield env.timeout(guide_time)
        if self.simulation.verbose:
            print(f"{self.name} llegó a {ma.points[point2]} en el tiempo {self.enviroment.get_time_of_day()}")
        
        self.current_position = point2
        if point2 != len(ma.points) - 2:
            self.update_beliefs()
            self.generate_desires()
            self.form_intentions()

            if "keep_walking" == self.intention:
                self.enviroment.mark[point2] = "continue"
                env.process(self.move(point2, point2 + 1, env, ma))
                self.simulation.cost += 0.5 * len(self.enviroment.excur)
            elif "setup_camp" == self.intention:
                self.enviroment.mark[point2] = "camp"
                env.process(self.enviroment.camp(point2)) 
                self.simulation.camp_points.append(ma.points[point2])
                self.simulation.cost += -2 * len(self.enviroment.excur)
            elif "have_lunch" == self.intention:
                self.enviroment.mark[point2] = "lunch"
                env.process(self.enviroment.lunch(point2)) 
                self.simulation.launch_points.append(ma.points[point2])
                self.simulation.cost += -1.5 * len(self.enviroment.excur)
            elif "regroup" == self.intention:
                self.enviroment.mark[point2] = "regroup"
                env.process(self.enviroment.regroup(point2))
                self.simulation.reagroup_points.append(ma.points[point2])
                self.simulation.cost += -1 * len(self.enviroment.excur)

    def update_beliefs(self):
        self.beliefs["time_of_day"] = self.enviroment.get_time_of_day()
        self.beliefs["dispersion"] = self.enviroment.calculate_dispersion()
        self.beliefs["had_lunch"] = 0 if self.enviroment.had_lunch else 1

    def generate_desires(self):
        self.desires = {
            "keep_together": False,
            "lunch": False,
            "camp": False
        }
        for rule in self.rules:
            if rule.evaluate(self.beliefs):
                for d in rule.desireset:
                    self.desires[d] = True

    def form_intentions(self):
        self.intention = ""
        intentions = []
        for di in self.dis:
            for d in di.desires:
                if not self.desires[d]:
                    continue
                intentions.append((di.priority, di.intention))
        intentions.sort()
        self.intention = intentions[0][1] if len(intentions) > 0 else "keep_walking"
        


class ExcursionAgent:
    def __init__(self, name, enviroment, desires, precomputed_data, simulation):
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
        self.precomputed_data = precomputed_data
        self.simulation = simulation
        

    def move(self, point1, point2, env, ma):
        waiting_time = self.precomputed_data[ma.points[point1]]["waiting_time"]

        yield env.timeout(ma.size[point1] / self.vel)
        
        if self.simulation.verbose:
            print(f"{self.name} llegó a {ma.points[point2]} en el tiempo {self.enviroment.get_time_of_day()}")

        self.current_position = point2
        
        desires_values = np.array(list(self.desires['point'].values())).reshape(1, -1)
        beliefs_values = np.array(list(self.precomputed_data[ma.points[point2]]["beliefs"].values())).reshape(1, -1)

        # Calcular la similitud coseno entre los dos vectores
        similarity = cosine_similarity(desires_values, beliefs_values)

        self.simulation.cost += -(similarity)
        if point2 != len(ma.points) - 2:
            
            if self.enviroment.mark[point2] == "regroup":
                env.process(self.enviroment.regroup(point2))
            elif self.enviroment.mark[point2] == "lunch":
                env.process(self.enviroment.lunch(point2))
            elif self.enviroment.mark[point2] == "camp":
                env.process(self.enviroment.camp(point2))
            else:
                # Si no es reagrupación, camp o almuerzo, continuar el movimiento normal
                yield env.timeout(waiting_time/60)
                env.process(self.move(point2, point2 + 1, env, ma))

    def reanudar(self, env, point1, point2, ma):
        # Reanudar el movimiento después de reagruparse, almorzar o acampar
        
        if self.simulation.verbose:
            print(f"{self.name} reanuda el movimiento desde {ma.points[point1]} hacia {ma.points[point2]}.")

        env.process(self.move(point1, point2, env, ma))


class Path:
    def __init__(self):
        self.points = []
        self.size = []  


