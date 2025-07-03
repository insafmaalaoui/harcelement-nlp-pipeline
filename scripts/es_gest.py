import pymongo
import os
import time
import socket
from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import RequestError, ConnectionError as ElasticsearchConnectionError
from langdetect import detect
from textblob import TextBlob

# Connexion MongoDB
mongo_host = os.environ.get("MONGO_HOST", "mongodb://mongodb:27017/")
print(f"ℹ️ Connecting to MongoDB at {mongo_host}")
try:
    client = pymongo.MongoClient(mongo_host)
    client.server_info()  # Test MongoDB connection
    print("✅ MongoDB connection successful")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    raise

db = client['harcelement']
collection = db['posts']

# Connexion Elasticsearch with retry
es_host = os.environ.get("ES_HOST", "http://localhost:9200")
print(f"ℹ️ Attempting to connect to Elasticsearch at {es_host}")
es = Elasticsearch(es_host, request_timeout=30)
# Nom de l’index
index_name = "harcelement_posts"

# Test DNS resolution
try:
    elasticsearch_ip = socket.gethostbyname('elasticsearch')
    print(f"✅ Resolved elasticsearch to IP: {elasticsearch_ip}")
except socket.gaierror as e:
    print(f"❌ Failed to resolve elasticsearch hostname: {e}")
    raise

# Retry connection to Elasticsearch
max_retries = 5
retry_interval = 5  # seconds
for attempt in range(max_retries):
    try:
        if es.ping():
            print("✅ Connected to Elasticsearch")
            break
        else:
            raise ElasticsearchConnectionError("Elasticsearch ping failed")
    except ElasticsearchConnectionError as e:
        if attempt < max_retries - 1:
            print(f"⚠️ Connection attempt {attempt + 1} failed: {e}. Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
        else:
            print(f"❌ Failed to connect to Elasticsearch after {max_retries} attempts: {e}")
            raise Exception("Elasticsearch server is not reachable")

# Vérifier ou créer l’index
try:
    if not es.indices.exists(index=index_name):
        mapping = {
            "mappings": {
                "properties": {
                    "titre": {"type": "text"},
                    "contenu": {"type": "text"},
                    "auteur": {"type": "keyword"},
                    "date": {"type": "date", "format": "strict_date_optional_time||epoch_millis"},
                    "url": {"type": "keyword"},
                    "langue": {"type": "keyword"},
                    "sentiment": {"type": "keyword"},
                    "score": {"type": "float"}
                }
            }
        }
        es.indices.create(index=index_name, body=mapping)
        print(f"✅ Index '{index_name}' créé.")
    else:
        print(f"ℹ️ Index '{index_name}' existe déjà.")
except RequestError as e:
    print(f"❌ Elasticsearch RequestError: {e.info}")
    raise
except Exception as e:
    print(f"❌ Failed to connect to Elasticsearch or check index: {e}")
    raise

# Fonction pour analyser le sentiment
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        sentiment = "positif"
    elif polarity < -0.1:
        sentiment = "negatif"
    else:
        sentiment = "neutre"
    return sentiment, round(polarity, 3)

# Récupérer les documents enrichis
try:
    posts = list(collection.find({"cleaned_text": {"$exists": True}}))
    print(f"🔍 {len(posts)} documents à indexer...")
except Exception as e:
    print(f"❌ Failed to retrieve documents from MongoDB: {e}")
    raise

# Préparer les documents pour Elasticsearch
actions = []

for post in posts:
    try:
        texte = post.get("cleaned_text", "")
        titre = post.get("titre", "") or f"Post {post.get('Id_post', '')[:8]}"
        auteur = post.get("auteur", "") or "anonyme"
        date = post.get("date", None)  # Format ISO ou None
        url = post.get("url", "") or None

        # Détection langue
        try:
            langue = detect(texte)
        except:
            langue = "unknown"

        # Sentiment
        try:
            sentiment, score = analyze_sentiment(texte)
        except:
            sentiment, score = "neutre", 0.0

        doc = {
            "_index": index_name,
            "_source": {
                "titre": titre,
                "contenu": texte,
                "auteur": auteur,
                "date": date,
                "url": url,
                "langue": langue,
                "sentiment": sentiment,
                "score": float(score)
            }
        }
        actions.append(doc)

    except Exception as e:
        print(f"⚠️ Erreur lors du traitement d’un document: {e}")

# Indexation en bulk
if actions:
    try:
        response = helpers.bulk(es, actions, raise_on_error=False)
        print(f"✅ {len(actions)} documents indexés dans Elasticsearch.")
        print("📦 Détails du bulk:", response)
    except Exception as e:
        print(f"❌ Bulk indexing failed: {e}")
        raise
else:
    print("❌ Aucun document à indexer.")