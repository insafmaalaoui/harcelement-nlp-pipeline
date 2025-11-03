# 🧠 Smart Conseil NLP Pipeline

A fully Dockerized Natural Language Processing (NLP) pipeline for scraping, cleaning, analyzing, and indexing social media posts using MongoDB, Elasticsearch, and Kibana.

---

## 📚 Overview

This project automates the end-to-end flow of collecting and processing social media data.

### Main Scripts

- scrapper.ipynb → Scrapes social media posts and stores them in MongoDB.
- nlp_pipeline.py → Cleans and preprocesses the scraped data, adds a cleaned_text field.
- nlp_processing.py → Performs NLP tasks (sentiment analysis, language detection, etc.).
- es_gest.py → Indexes processed data into Elasticsearch.

---

## ⚙️ Prerequisites

Make sure you have the following installed:

- Docker Desktop (Windows / macOS / Linux)
- Docker Compose (v2.0 or higher recommended)
- Python 3.10 (already included inside the container)

### Project Structure

test_smart_conseil/
├── docker-compose.yml
├── Dockerfile
├── docker-volume/
│   ├── scripts/              # Contains pipeline scripts
│   ├── Screenshots/          # Stores screenshots (optional)
│   └── exports_data/         # Stores exported data (optional)

---

## 🚀 Setup Instructions

1️⃣ Clone the Repository

git clone <repository-url>
cd test_smart_conseil

2️⃣ Prepare the Scripts Directory

Ensure all four scripts are available:

mkdir -p ./docker-volume/scripts

Copy the following into ./docker-volume/scripts/:

scrapper.ipynb  
nlp_pipeline.py  
nlp_processing.py  
es_gest.py  

3️⃣ Create the Pipeline Runner (run_all.sh)

echo -e '#!/bin/bash\njupyter nbconvert --to python --output scrapper.py scrapper.ipynb\npython scrapper.py\npython nlp_pipeline.py\npython nlp_processing.py\npython es_gest.py' > ./docker-volume/scripts/run_all.sh

docker run --rm -v scripts:/target -v "$(pwd)/docker-volume/scripts:/source" busybox sh -c "cp /source/run_all.sh /target/ && chmod +x /target/run_all.sh"

4️⃣ Build the Docker Image

docker compose build --no-cache smartconseil-app

5️⃣ Start the Services

Run the containers in order:

docker compose down  
docker rm -f smartconseil-app kibana elasticsearch mongodb  
docker compose up -d mongodb  
docker compose up -d elasticsearch  
docker compose up -d kibana  
docker compose up -d smartconseil-app  

6️⃣ Verify Setup

docker ps  

Ensure that mongodb, elasticsearch, kibana, and smartconseil-app are all running and healthy.

---

## 💡 Usage

The smartconseil-app container executes the full pipeline via run_all.sh.

Step 1 → scrapper.ipynb: Scrapes posts and stores them in MongoDB (harcelement.posts)  
Step 2 → nlp_pipeline.py: Cleans the data, adds cleaned_text  
Step 3 → nlp_processing.py: Performs NLP tasks (sentiment analysis, language detection)  
Step 4 → es_gest.py: Indexes processed data into Elasticsearch (harcelement_posts index)

Check logs for execution details:

docker logs smartconseil-app

---

## 🗃️ Accessing Databases

MongoDB:

docker exec -it mongodb mongosh mongodb://mongodb:27017/harcelement  
db.posts.find({"cleaned_text": {$exists: true}}).count()  

Elasticsearch:

docker exec -it smartconseil-app curl http://elasticsearch:9200/harcelement_posts/_count  

Kibana:

Open http://localhost:5601 to visualize the harcelement_posts index.

---

## 🧭 Keeping the Container Running

If you need smartconseil-app to stay running for debugging:

Edit docker-compose.yml:

command: /bin/bash -c "/app/run_all.sh && tail -f /dev/null"

Restart the container:

docker compose down  
docker compose up -d smartconseil-app  

---

## 🧰 Troubleshooting

No Documents Indexed:

If logs show “0 documents à indexer”, verify that the preprocessing scripts populate cleaned_text in MongoDB.

docker logs smartconseil-app

Manually inspect MongoDB:

docker exec -it mongodb mongosh mongodb://mongodb:27017/harcelement  
db.posts.find().pretty()  

Elasticsearch Connection Issues:

docker run --rm -it --network test_smart_conseil_default test_smart_conseil-smartconseil-app curl http://elasticsearch:9200

docker logs elasticsearch

Notebook Execution Errors:

docker run --rm -it --network test_smart_conseil_default test_smart_conseil-smartconseil-app bash  
jupyter nbconvert --to python --output scrapper.py scrapper.ipynb  
python scrapper.py  

---

## 📦 Dependencies

Docker Images:
- mongo:latest  
- docker.elastic.co/elasticsearch/elasticsearch:8.13.4  
- docker.elastic.co/kibana/kibana:8.13.4  
- Custom smartconseil-app (built from python:3.10-slim)

Python Packages (in smartconseil-app):
- pymongo  
- elasticsearch==8.13.2  
- langdetect  
- textblob  
- spacy  
- jupyter  
- requests  
- beautifulsoup4  

---

## 🗒️ Notes

- Ensure scrapper.ipynb is configured to store data in the harcelement.posts collection in MongoDB.  
- Add any additional dependencies for scrapper.ipynb to the Dockerfile if required.  
- exports_data/ and Screenshots/ directories are optional for storing outputs and images.

---

## 👩‍💻 Author

**Insaf Maaloui**  
Data Science & AI Student – TEK-UP University  
📧 insaf.maaloui@example.com  

---

✅ End of README
