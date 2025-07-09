#!/bin/bash
jupyter nbconvert --to python --output scraper.py scraper..ipynb
python scraper.py
python nlp_pipeline.py
python preprocessing.py
python es_gest.py
echo "run_all.sh terminé avec succès"


