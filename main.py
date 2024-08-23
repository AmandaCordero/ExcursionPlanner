from modules import module_0, module_1, module_2
from utils.map_utils import *
import random

def main():
    # Load map (Replace this with actual map loading logic)
    map_data = Map()

    # Assume survey responses are collected and stored in survey_responses
    # survey_responses = "path_to_survey_responses"

    # Module 0: Process survey responses to get characteristics
    characteristics = module_0.get_characteristics()
    # print("Characteristics:\n", characteristics, '\n')

    # Module 1: Generate route based on map and characteristics
    route = module_1.plan_route(map_data, characteristics)
    print("Route:\n", route)

    # # Module 2: Calculate resources needed for the route
    # resources = module_2.calculate_resources(route, characteristics)
    # print("Resources needed:", resources)


class Point:
    def __init__(self, location, name="", characteristics=[], IsRest=False):
        self.name = name # puede que el punto tenga un nombre en particular
        self.characteristics = characteristics  # conjunto donde a cada aspecto para los turistas se le asocia un nivel de relevancia
        self.rest = IsRest # lugar de descanso
        self.location = location
    
    def set_characteristics(self, characteristics):
        '''
            Permite establecer características del terreno
            y su relevancia. 
            
            Recibe 'characteristics' que es un array de tuplas (string,num)
            donde el primer elemento es el nombre de la característica y el segundo
            es el nivel de relevancia.
        '''
        
        for characteristic in characteristics:
            self.characteristics.append((characteristic[0],characteristic[1]))


if __name__ == "__main__":
    main()

    # ma = [
    #     [1,2],
    #     [3,4]
    # ]

    # print(ma[0][1]) 
    # (imprime 2)

    # sierra = Map()
    # print(sierra)
    



