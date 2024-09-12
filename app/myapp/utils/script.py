# Cargamos los datos de los turistas
import json

    # {
    #     "id": 1,
    #     "x": 1.0,
    #     "y": 1.0,
    #     "height": 1.0,
    #     "point_id": 1,
    #     "characteristics": [
    #         1.0,
    #         1.0,
    #         1.0,
    #         1.0
    #     ],
    #     "begin": true,
    #     "finish": false,
    #     "interesting": false
    # }

new_edges = []
with open('./edges_data.json', 'r') as file:
    edges = json.load(file)
i = 0
for edge in edges:
    
    characteristics = [0,0]
    if edge['characteristics']:
        characteristics = edge['characteristics'][:2]
        interesting = True
    
    new_edges.append(
        {
            'id': i,
            'point1': edge['point1'],
            'point2': edge['point2'],
            'distance': edge['distance'],
            'characteristics': characteristics+ [0,0,0,0]
        }
    )
    
    i += 1


with open('./new_edges_data.json', 'w') as file:
    json.dump(new_edges, file, indent=4)