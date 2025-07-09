#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import uuid
from pymongo import MongoClient


# In[ ]:





# In[ ]:


df = pd.read_csv("Cyberbullying.csv") 
print(f"[INFO] Nombre de lignes : {len(df)}")


# In[7]:


df


# #### Harmoniser les valeurs du champ 'label'

# In[10]:


df['Label'] = df['Label'].str.lower().str.replace('not - bullying', 'not-bullying').str.strip()


# In[12]:


df


# ####  Supprimer les lignes vides 

# In[15]:


df = df.dropna(subset=['Text', 'Label'])


# In[17]:


df


# In[19]:


df.isnull().sum()


# #### Ajouter un ID unique par message

# In[22]:


df['Id_post'] = [str(uuid.uuid4()) for _ in range(len(df))]


# In[ ]:


client = MongoClient('mongodb://mongodb:27017/')
db = client['harcelement']
collection = db['posts']
collection.delete_many({})  # si tu veux réinitialiser
collection.insert_many(df[['Id_post', 'Text', 'Types', 'Label']].to_dict(orient='records'))


# In[ ]:




