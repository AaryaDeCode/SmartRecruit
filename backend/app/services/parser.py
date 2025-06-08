# services/parser.py

import os
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import networkx as nx
from transformers import pipeline

# NER Pipeline
ner_model = pipeline("ner", model="dslim/bert-base-NER", grouped_entities=True)

def extract_text_from_resume(file_path: str) -> str:
    text = ''
    if file_path.endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + ' '
    if not text.strip():
        images = convert_from_path(file_path)
        for img in images:
            text += pytesseract.image_to_string(img) + ' '
    return text

def extract_entities(text: str) -> dict:
    entities = ner_model(text)
    extracted = {}
    for ent in entities:
        label = ent['entity_group']
        word = ent['word']
        if label not in extracted:
            extracted[label] = []
        extracted[label].append(word)
    return extracted

def build_knowledge_graph(entities: dict) -> nx.Graph:
    G = nx.Graph()
    for entity_type, values in entities.items():
        for val in values:
            G.add_node(val, label=entity_type)
    if 'ORG' in entities and 'JOB' in entities:
        for org in entities['ORG']:
            for job in entities['JOB']:
                G.add_edge(org, job)
    if 'SKILL' in entities and 'JOB' in entities:
        for skill in entities['SKILL']:
            for job in entities['JOB']:
                G.add_edge(skill, job)
    return G
