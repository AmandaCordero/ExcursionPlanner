class Tourist_Statistic:
    def __init__(self, name, very_preferences, normal_preferences, stamine):
        self.name = name
        self.very_preferences = very_preferences
        self.normal_preferences = normal_preferences 
        self.stamine = stamine

def get_characteristics():
    '''
        Recibe un array de `Tourist_Statistic` con los resultados de la encuesta para cada turista
    '''

    survey_responses = [
        Tourist_Statistic('pablo', ['A','B'], ['C'],7), 
        Tourist_Statistic('pablo', ['A'], ['D'],5)
    ]

    # Diccionario con las caracteristicas que utilizará el algoritmo para evaluar el mejor
    # camino. Tendrá como key un aspecto relevante de los turistas (pantano, ríos, plantas
    # exóticas, etc) y como value una dupla (count, ave_stamine) donde count será la
    # cantidad de personas que tienen esa característica y el promedio de estamina de cada una
    characteristics = {}

    for result in survey_responses:
        for item in result.very_preferences:
            if item in characteristics:
                count,stamine = characteristics[item]
                characteristics[item] = (count+2, stamine+2*result.stamine)
            else:
                characteristics[item] = (2,2*result.stamine)
        
        for item in result.normal_preferences:
            if item in characteristics:
                count,stamine = characteristics[item]
                characteristics[item] = (count+1, stamine+result.stamine)
            else:
                characteristics[item] = (1,result.stamine)

    # Input:
    # [
    #    Tourist_Statistic('pablo', ['A','B'], ['C'],7), 
    #    Tourist_Statistic('pablo', ['A'], ['D'],5)
    # ]
    #
    # Output: 
    # {'A': (4, 24), 'B': (2, 14), 'C': (1, 7), 'D': (1, 5)}
    return characteristics