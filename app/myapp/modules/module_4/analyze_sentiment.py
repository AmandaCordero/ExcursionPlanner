import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

# Crear el lematizador y las stopwords
stemmer = SnowballStemmer('spanish')
stop_words = set(stopwords.words('spanish'))

# Lematizar el léxico
def lemmatize_lexicon(lexicon):
    lemmatized_lexicon = {}
    for word, score in lexicon.items():
        lemmatized_word = stemmer.stem(word)
        lemmatized_lexicon[lemmatized_word] = score
    return lemmatized_lexicon

def preprocess_text(text):
    # Convertir a minúsculas
    text = text.lower()
    # Eliminar puntuación y caracteres especiales
    text = re.sub(r'[^\w\s]', '', text)
    # Dividir en palabras
    words = text.split()
    # Eliminar stop words y aplicar lematización
    words = [stemmer.stem(word) for word in words if word not in stop_words]
    return words

def generate_ngrams(words, n=2):
    ngrams = zip(*[words[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]

def calculate_sentiment(words, lexicon):
    total_sentiment = 0.0
    skip_next = False
    bigrams = generate_ngrams(words)
    trigrams = generate_ngrams(words, 3)
    words = words + bigrams + trigrams

    for i, word in enumerate(words):
        if skip_next:
            skip_next = False
            continue
        if word in lexicon:
            if i > 0 and words[i-1] in ["no", "nunca", "jamás", "sin embargo"]:
                total_sentiment += lexicon[word] * -1
                skip_next = True
            elif i > 0 and words[i-1] in ["muy", "extremadamente"]:
                total_sentiment += lexicon[word] * 1.5
            else:
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

    # Lematizar el léxico original
    lemmatized_lexicon_es = lemmatize_lexicon(lexicon)

    words = preprocess_text(text)
    sentiment_score = calculate_sentiment(words, lemmatized_lexicon_es)
    sentiment = classify_sentiment(sentiment_score)
    print(f"Sentimiento: {sentiment}, Score: {sentiment_score}")
    return sentiment, sentiment_score
