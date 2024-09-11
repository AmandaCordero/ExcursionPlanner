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

new_points = []
with open('./points_data.json', 'r') as file:
    points = json.load(file)['points']
i = 0
for point in points:
    
    begin = False
    finish = False
    interesting = False
    
    characteristics = [0,0,0,0]
    if point['characteristics']:
        characteristics = point['characteristics'][2:]
        interesting = True
    
    if point['id'] == 58:
        finish = True
    elif point['id'] == 0:
        begin = True
        
    new_points.append(
        {
            'id': i,
            'point_id': point['id'],
            'x': point['location'][0],
            'y': point['location'][1],
            'height': point['height'],
            'characteristics': characteristics,
            'begin': begin,
            'finish': finish,
            'interesting': interesting
        }
    )
    
    i += 1


with open('./new_points_data.json', 'w') as file:
    json.dump(new_points, file, indent=4)