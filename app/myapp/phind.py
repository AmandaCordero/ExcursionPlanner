from mistralai import Mistral

def phind(points):
    MISTRAL_API_KEY='amk4WhcFI6dXBHJUzcjhQhwUhmgjMqlP'
    client = Mistral(api_key=MISTRAL_API_KEY)

    prompt = (
        "Imagina que estás creando un comercial emocionante para una excursión en un hermoso paisaje natural. "
        "Los visitantes recorrerán diversos puntos, cada uno con sus propios encantos. "
        "Debes describir estos lugares de manera atractiva y destacar las experiencias únicas que pueden ofrecer para que los turistas se sientan emocionados. "
        "Aquí están los puntos del recorrido:"
    )

    # Generar respuestas para cada punto
    for point in points:
        Id = point["id"]
        location = point["location"]
        altitude = point["height"]
        char1 = point["characteristics"][0]
        char2 = point["characteristics"][1]
        char3 = point["characteristics"][2]
        char4 = point["characteristics"][3]

        fauna_desc = f"con un índice de diversidad de fauna de {char1}"
        flora_desc = f"con un índice de variedad de flora de {char2}"
        rivers_desc = f"con un índice de ríos de {char3}"
        historic_desc = f"con un índice de historia de {char4}"

        prompt += (
            f"\nPunto {Id}: Ubicado en {location}, es un lugar a {altitude} altitud. "
            f"Este lugar es {fauna_desc}, {flora_desc}, {rivers_desc}, y {historic_desc}. "
            "Un lugar que promete una experiencia enriquecedora."
        )

    prompt += "\nCambia los porcentajes de interés de cada caracteristicas por palabras que den a entender las más relevantes, e inventa detalles relacionados a estas."
    prompt += "\nElabora un mini-comercial sobre esta excursión, pero quiero solo el texto."

    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    
    # Construir el prompt basado en los puntos de interés
    points = [{
        "id": 32,
        "location": [886,747],
        "characteristics": [0.6, 0.4, 0, 0.2, 0, 0],
        "altitude": "low",
        "height": 10
    },
    {
        "id": 36,
        "location": [1230,413],
        "characteristics": [0.9, 0.8, 0.4, 0, 0, 0.5],
        "altitude": "top",
        "height": 120
    },
    {
        "id": 55,
        "location": [1744,730],
        "characteristics": [0.9, 0.4, 0.3, 0.7, 0, 0.3],
        "altitude": "low",
        "height": 10
    },
    {
        "id": 60,
        "location": [1760,45],
        "characteristics": [0.8, 0.1, 0, 0.2, 0, 0.8],
        "altitude": "low",
        "height": 6
    }]
    
    print(phind(points))