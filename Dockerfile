# Image de base Python
FROM python:3.10-slim

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copier tout le code source dans le conteneur
COPY ./scripts /app
COPY ./Screenshots /Screenshots
COPY ./exports_data /exports_data

# Installer les dépendances système nécessaires
RUN apt-get update && \
    apt-get install -y build-essential gcc && \
    apt-get clean

# Installer les dépendances Python
RUN pip install --upgrade pip
RUN pip install elasticsearch==8.13.2
RUN pip install \
    pymongo \
    langdetect \
    textblob \
    jupyter \
    spacy \
    requests \
    beautifulsoup4 \
    pandas \
    uuid  \
    uvicorn[standard] \
    fastapi

# Télécharger les données de TextBlob
RUN python -m textblob.download_corpora
RUN python -m spacy download en_core_web_sm --no-cache-dir || { echo "SpaCy model download failed"; exit 1; }

# Point d'entrée (script à exécuter automatiquement)
CMD bash -c "/app/run_all.sh && uvicorn fastapi_app:app --host 0.0.0.0 --port 8000"

