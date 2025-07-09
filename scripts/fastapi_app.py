from fastapi import FastAPI
from pydantic import BaseModel
from textblob import TextBlob
from langdetect import detect
import spacy

app = FastAPI()
nlp = spacy.load("en_core_web_sm")

class InputText(BaseModel):
    text: str

@app.post("/analyze")
def analyze_text(data: InputText):
    text = data.text

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        sentiment = "positive"
    elif polarity < -0.1:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    try:
        language = detect(text)
    except:
        language = "unknown"

    lemmatized = " ".join([token.lemma_ for token in nlp(text)])

    return {
        "text": text,
        "language": language,
        "sentiment": sentiment,
        "polarity": polarity,
        "lemmatized": lemmatized
    }
