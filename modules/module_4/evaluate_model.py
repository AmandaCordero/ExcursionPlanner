from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from analyze_sentiment import analyze_sentiment
from dataset import sentiment_lexicon_es
from dataset import test_data


def evaluate_model(test_data, lexicon):
    y_true = []
    y_pred = []
    
    for entry in test_data:
        review = entry['review']
        true_label = entry['label']
        predicted_label, _ = analyze_sentiment(review, lexicon)
        
        y_true.append(true_label)
        y_pred.append(predicted_label)
    
    # Cálculo de las métricas
    precision = precision_score(y_true, y_pred, average='macro')
    recall = recall_score(y_true, y_pred, average='macro')
    f1 = f1_score(y_true, y_pred, average='macro')
    accuracy = accuracy_score(y_true, y_pred)
    
    return precision, recall, f1, accuracy

# Evaluar el modelo

precision, recall, f1, accuracy = evaluate_model(test_data, sentiment_lexicon_es)
print(f"Precisión: {precision}")
print(f"Recall: {recall}")
print(f"F1-Score: {f1}")
print(f"Exactitud: {accuracy}")
