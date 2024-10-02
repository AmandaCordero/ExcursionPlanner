import simpy
import numpy as np
from defuzzification_module import compute_fuzzy_output

class Simulation:

    def __init__(self):
        self.camp_points = []
        self.reagroup_points = []
        self.launch_points = []

    def simulate_excursion(self, desires, route, map, precomputed_data):

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

        # Crear más excursionistas para un caso más grande
        guide = GuideAgent(None, self)  # El entorno aún no se asigna
        excursion_agents = []

        for i in range(len(desires)):
            excursion_agents.append(ExcursionAgent(f'exc{i}', None, desires[i], precomputed_data))

        environment = Enviroment(guide, excursion_agents, path, env, map)

        # Asignar el entorno a los agentes
        guide.enviroment = environment
        for exc in excursion_agents:
            exc.enviroment = environment

        # Ejecutar los procesos de movimiento
        env.process(guide.move(0, 1, env, path))
        for exc in excursion_agents:
            env.process(exc.move(0, 1, env, path))

        env.run()

        return self.camp_points, self.reagroup_points, self.launch_points


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
        if self.regroup_count == len(self.excur) + 1:
            print(f"Todos los excursionistas han llegado al punto de reagrupación {point}.")
            self.regroup_count = 0  # Reiniciar el contador
            # Reanudar el movimiento de todos los excursionistas
            self.env.process(self.guide.move(point, point + 1, self.env, self.path))
            for exc in self.excur:
                exc.reanudar(self.env, point, point + 1, self.path)
    
    def lunch(self, point):
        # Verificar si todos los excursionistas han llegado al punto de almuerzo
        self.lunch_count += 1
        if self.lunch_count == len(self.excur) + 1:
            print(f"Todos los excursionistas han llegado al punto de almuerzo {point}.")
            self.had_lunch = True
            self.lunch_count = 0  # Reiniciar el contador
            # Reanudar el movimiento de todos los excursionistas
            
            yield self.env.timeout(0.5)
            self.env.process(self.guide.move(point, point + 1, self.env, self.path))
            for exc in self.excur:
                exc.reanudar(self.env, point, point + 1, self.path)
    
    def camp(self, point):
        # Verificar si todos los excursionistas han llegado al punto de campamento
        self.camp_count += 1
        if self.camp_count == len(self.excur) + 1:
            print(f"Todos los excursionistas han llegado al campamento en {point}.")
            self.camp_count = 0  # Reiniciar el contador
            # Reanudar el movimiento de todos los excursionistas
            
            yield self.env.timeout(10)
            self.had_lunch = False
            self.env.process(self.guide.move(point, point + 1, self.env, self.path))
            for exc in self.excur:
                exc.reanudar(self.env, point, point + 1, self.path)


class GuideAgent:
    def __init__(self, enviroment, simulation):
        self.name = "el guia"
        self.beliefs = {}
        self.desires = {}
        self.intentions = []
        self.enviroment = enviroment
        self.current_position = 0
        self.simulation = simulation
        
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
        print(f"{self.name} llegó a {ma.points[point2]} en el tiempo {self.enviroment.get_time_of_day()}")
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
                self.simulation.camp_points.append(point2)
            elif "have_lunch" in self.intentions:
                self.enviroment.mark[point2] = "lunch"
                env.process(self.enviroment.lunch(point2))  # Lógica para almorzar
                self.simulation.launch_points.append(point2)
            elif "regroup" in self.intentions:
                self.enviroment.mark[point2] = "regroup"
                self.enviroment.regroup(point2)  # Reagrupar
                self.simulation.reagroup_points.append(point2)

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
    def __init__(self, name, enviroment, desires, precomputed_data):
        self.name = name
        self.vel = np.random.uniform(2, 3)
        self.beliefs = {}
        self.desires = {}
        self.desires["point"] = {
            'user_flora': desires[2],
            'user_fauna': desires[3],
            'user_history': desires[4],
            'user_rivers': desires[5]
        }
        self.desires["path"] = {
            'user_isolation': desires[0],
            'user_challenge': desires[1],
            'user_flora': desires[2],
            'user_fauna': desires[3]
        }
        
        self.intentions = {}
        self.current_position = 0
        self.enviroment = enviroment
        self.precomputed_data = precomputed_data

    def move(self, point1, point2, env, ma):
        waiting_time = self.precomputed_data[point1]["waiting_time"]

        yield env.timeout(ma.size[point1] / self.vel)
        print(f"{self.name} llegó a {ma.points[point2]} en el tiempo {self.enviroment.get_time_of_day()}")
        self.current_position = point2
        if point2 != len(ma.points) - 1:
            
            if self.enviroment.mark[point2] == "regroup":
                self.enviroment.regroup(point2)
            elif self.enviroment.mark[point2] == "lunch":
                env.process(self.enviroment.lunch(point2))
            elif self.enviroment.mark[point2] == "camp":
                env.process(self.enviroment.camp(point2))
            else:
                # Si no es reagrupación, camp o almuerzo, continuar el movimiento normal
                yield env.timeout(waiting_time / 60)
                env.process(self.move(point2, point2 + 1, env, ma))

    def reanudar(self, env, point1, point2, ma):
        # Reanudar el movimiento después de reagruparse, almorzar o acampar
        print(f"{self.name} reanuda el movimiento desde {ma.points[point1]} hacia {ma.points[point2]}.")
        env.process(self.move(point1, point2, env, ma))


class Path:
    def __init__(self):
        self.points = []
        self.size = [] 


def main():
    # Definición del mapa y la ruta
    map = Map()
    map.edges_size = {('A', 'B'): 10, ('B', 'C'): 15, ('C', 'D'): 20}  # Distancias entre los puntos del mapa
    map.points = ['A', 'B', 'C', 'D']

    # Definir la ruta que tomarán los excursionistas
    route = ['A', 'B', 'C', 'D']

    # Definir deseos de los excursionistas: [isolation, challenge, flora, fauna, history, rivers]
    desires = [
        [3, 2, 4, 3, 1, 2],  # Excursionista 1
        [2, 3, 3, 4, 2, 1],  # Excursionista 2
        [4, 1, 2, 3, 3, 2]   # Excursionista 3
    ]

    # Datos precomputados de los excursionistas (tiempos de espera en cada punto)
    precomputed_data = {
    0: {"waiting_time": [5, 6, 7]},  # Tiempos de espera en el punto 0 para cada excursionista
    1: {"waiting_time": [3, 4, 5]},  # Tiempos de espera en el punto 1 para cada excursionista
    2: {"waiting_time": [4, 5, 6]},  # Tiempos de espera en el punto 2 para cada excursionista
    3: {"waiting_time": [2, 3, 4]}   # Tiempos de espera en el punto 3 para cada excursionista
}



    # Crear instancia de la simulación
    simulation = Simulation()

    # Ejecutar la simulación con los deseos, la ruta, el mapa y los datos precomputados
    camp_points, reagroup_points, launch_points = simulation.simulate_excursion(desires, route, map, precomputed_data)

    # Imprimir resultados de la simulación
    print("Puntos de campamento:", camp_points)
    print("Puntos de reagrupamiento:", reagroup_points)
    print("Puntos de almuerzo:", launch_points)


class Map:
    def __init__(self):
        self.points = []
        self.edges_size = {}


if __name__ == "__main__":
    main()
