from modules import module_1, module_2
# from modules.module_0 import characteristics
from utils.map_utils import Map

def main():
    # Load map (Replace this with actual map loading logic)
    map_data = Map()

    # # Assume survey responses are collected and stored in survey_responses
    # survey_responses = "path_to_survey_responses"

    # # Module 0: Process survey responses to get characteristics
    # characteristics = characteristics.get_characteristics(survey_responses)
    # print("Characteristics:", characteristics)
    
    characteristics = [
        [0, 0, 0, 0, 0, 0.8],
        [0, 0, 0, 0, 0, 0.8],
        [0, 0, 0, 0, 0, 0.8],
        [0, 0, 0, 0, 0, 0.8]
    ]

    # Module 1: Generate route based on map and characteristics
    route = module_1.plan_route(map_data, characteristics)
    print("Route:", route)

    # # Module 2: Calculate resources needed for the route
    # resources = module_2.calculate_resources(route, characteristics)
    # print("Resources needed:", resources)

if __name__ == "__main__":
    main()