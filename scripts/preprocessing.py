import re
import pymongo
import nltk
from nltk.corpus import stopwords
import spacy
from tqdm import tqdm
import os

# Télécharger les ressources NLTK au premier lancement
nltk.download('stopwords')
nltk.download('punkt')

# Charger le modèle spacy pour l'anglais
nlp = spacy.load("en_core_web_sm")

# Liste des stopwords en anglais
stop_words = set(stopwords.words('english'))

# Connexion MongoDB
mongo_host = os.environ.get("MONGO_HOST", "mongodb://mongodb:27017/")
client = pymongo.MongoClient(mongo_host)
db = client['harcelement']
collection = db['posts']

def clean_text(text):
    if not isinstance(text, str) or not text.strip():
        return ""
    
    text = text.lower()
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)  # Supprimer URLs
    text = re.sub(r'[^a-z\s]', '', text)  # Garder lettres et espaces uniquement

    tokens = nltk.word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]

    doc = nlp(' '.join(tokens))
    lemmas = [token.lemma_ for token in doc]

    return ' '.join(lemmas)

# Récupérer documents sans cleaned_text pour éviter traitement inutile
posts = list(collection.find({"cleaned_text": {"$exists": False}}))

print(f"Nombre de posts à traiter : {len(posts)}")

for post in tqdm(posts):
    raw_text = post.get('Text', '')  # Attention à la casse du champ dans la BDD
    if raw_text.strip():
        cleaned = clean_text(raw_text)
    else:
        cleaned = ""
    collection.update_one({'_id': post['_id']}, {'$set': {'cleaned_text': cleaned}})

print("Prétraitement terminé et mis à jour dans MongoDB.")