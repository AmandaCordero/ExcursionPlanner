import re
from sentiment_lexicon_es import sentiment_lexicon_es

def preprocess_text(text):
    # Convertir a minúsculas
    text = text.lower()
    # Eliminar puntuación y caracteres especiales
    text = re.sub(r'[^\w\s]', '', text)
    # Dividir en palabras
    words = text.split()
    return words


def calculate_sentiment(words, lexicon):
    total_sentiment = 0.0
    for i, word in enumerate(words):
        if word in lexicon:
            total_sentiment += lexicon[word]
    return total_sentiment


def classify_sentiment(sentiment_score):
    if sentiment_score > 0:
        return "Positivo"
    elif sentiment_score < 0:
        return "Negativo"
    else:
        return "Neutral"


def analyze_sentiment(text, lexicon):
    words = preprocess_text(text)
    sentiment_score = calculate_sentiment(words, lexicon)
    sentiment = classify_sentiment(sentiment_score)
    return sentiment, sentiment_score

# Ejemplo de uso
review = "La acampada fue increíble, el paisaje era hermoso y la experiencia muy relajante. Sin embargo, la tienda era incómoda y el camino estuvo peligroso."
sentiment, score = analyze_sentiment(review, sentiment_lexicon_es)
print(f"Sentimiento: {sentiment}, Score: {score}")
