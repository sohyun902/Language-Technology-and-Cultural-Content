import joblib
import chardet
from konlpy.tag import Kkma
from functions.preprocessing import space, clean_korean_documents 

kkma = Kkma()

def load_model(model_path='./model.joblib', vectorizer_path='./vectorizer.joblib'):
    try:
        lr_model = joblib.load(model_path)
        tfidf_vectorizer = joblib.load(vectorizer_path)
        return lr_model, tfidf_vectorizer
    except FileNotFoundError:
        print("Model or vectorizer file not found. Please train the model first.")
        return None, None

def preprocess_and_tokenize(contents):
    processed_contents = []
    for content in contents:
        if not isinstance(content, str) or not content:
            processed_contents.append([])
            continue
        encode=chardet.detect(content.encode())
        if encode["encoding"]==None:
            continue

        content = content.strip()
        content = content.replace(" ", "")
        content = content.replace("\n", "")
        content = content.replace("\u200b", "")

        sents = kkma.sentences(content)
        spaced_sents = [space(sent) for sent in sents]
        cleaned_sents = clean_korean_documents(spaced_sents)
        processed_contents.append(cleaned_sents)
    return processed_contents


def analyze_sentiment(sentences, model, vectorizer):
    if not sentences:
        return []
    try:
        sentence_vectors = vectorizer.transform(sentences)
        predictions = model.predict(sentence_vectors)
        return predictions
    except ValueError as e:
        print(f"Error during sentiment analysis: {e}")
        print("This might be due to unseen words or issues with the input sentences.")
        return [] 