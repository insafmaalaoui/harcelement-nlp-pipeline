#!/bin/bash
jupyter nbconvert --to python --output scraper.py scraper..ipynb
python scraper.py
python nlp_pipeline.py
python preprocessing.py
python es_gest.py

