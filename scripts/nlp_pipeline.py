from pymongo import MongoClient
from langdetect import detect
from textblob import TextBlob
from tqdm import tqdm
import os

# Connexion MongoDB
mongo_host = os.environ.get("MONGO_HOST", "mongodb://mongodb:27017/")
client = MongoClient(mongo_host)
db = client['harcelement']
collection = db['posts']  
# On cible uniquement les documents qui n'ont pas encore la langue détectée
query = {"language": {"$exists": False}}

documents = collection.find(query)

for doc in tqdm(documents):
    text = doc.get("Text", "")
    if not text.strip():
        print(f"Document {doc['_id']} vide, on passe.")
        continue

    try:
        # Détection de la langue
        lang = detect(text)

        # Analyse de sentiment avec TextBlob
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        # Mise à jour dans la base
        update_result = collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"language": lang, "sentiment": sentiment}}
        )

        if update_result.modified_count == 1:
            print(f"Document {doc['_id']} mis à jour : langue={lang}, sentiment={sentiment}")
        else:
            print(f"Document {doc['_id']} non modifié.")

    except Exception as e:
        print(f"Erreur sur document {doc['_id']} : {e}")

print("Traitement NLP terminé.")