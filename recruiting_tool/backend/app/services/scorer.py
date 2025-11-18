# services/scorer.py

import torch
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv, global_mean_pool
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
import google.generativeai as genai

# Device
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# SBERT model
sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

# Sentiment Analysis
sentiment_model = pipeline("sentiment-analysis")

# --- GCN Model ---
class GCN(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, output_dim)

    def forward(self, x, edge_index, batch):
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = self.conv2(x, edge_index)
        x = global_mean_pool(x, batch)
        return x

gcn_model = GCN(input_dim=384, hidden_dim=128, output_dim=64).to(device)

# --- Gemini API ---
GEMINI_API_KEY = 'AIzaSyDy7yR0srhPp4TKj7QjZlOVim52csF0PvU'  # <-- Replace in real setup
genai.configure(api_key=GEMINI_API_KEY)

def get_keywords_from_gemini(jd_text: str) -> list:
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = f"Actually I am building context aware resume filtering tool ,So Extract the  related keywords like skills, tools, technologies from this Job Description:\n{jd_text}\nOnly give comma-separated keywords."
    response = model.generate_content(prompt)
    keywords = response.text.strip().split(',')
    return [k.strip() for k in keywords]

def semantic_similarity(text1: str, text2: str) -> float:
    emb1 = sbert_model.encode(text1, convert_to_tensor=True)
    emb2 = sbert_model.encode(text2, convert_to_tensor=True)
    return util.cos_sim(emb1, emb2).item()

def graph_to_data(graph):
    node_attrs = list(graph.nodes(data=True))
    node_labels = [node for node, attr in node_attrs]
    node_features = []
    for label in node_labels:
        emb = sbert_model.encode(label)
        node_features.append(emb)
    node_features = torch.tensor(node_features, dtype=torch.float)

    edges = list(graph.edges())
    if edges:
        edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
    else:
        edge_index = torch.empty((2, 0), dtype=torch.long)

    return Data(x=node_features, edge_index=edge_index)

def graph_embedding(G, model) -> torch.Tensor:
    if G.number_of_nodes() == 0:
        G.add_node("DUMMY", label="DUMMY")
    data = graph_to_data(G).to(device)
    batch = torch.zeros(data.x.size(0), dtype=torch.long).to(device)
    with torch.no_grad():
        embedding = model(data.x, data.edge_index, batch)
    return embedding.squeeze()

def rule_based_score(resume_text: str, job_keywords: list) -> float:
    hits = 0
    resume_text = resume_text.lower()
    for keyword in job_keywords:
        if keyword.lower() in resume_text:
            hits += 1
    return hits / len(job_keywords) if job_keywords else 0

def cultural_fit_score(text: str) -> float:
    result = sentiment_model(text[:512])[0]
    return 1.0 if result['label'] == 'POSITIVE' else 0.5

def final_score(resume_text: str, jd_text: str, resume_graph, jd_graph, model, keywords: list):
    sem_score = semantic_similarity(resume_text, jd_text)
    resume_emb = graph_embedding(resume_graph, model)
    jd_emb = graph_embedding(jd_graph, model)
    graph_score = cosine_similarity(resume_emb.cpu().reshape(1, -1), jd_emb.cpu().reshape(1, -1))[0][0]
    rule_score = rule_based_score(resume_text, keywords)
    culture_score = cultural_fit_score(resume_text) * 0.1

    final = 0.5 * sem_score + 0.2 * graph_score + 0.3 * rule_score + 0 * culture_score
    return [sem_score, graph_score, rule_score, culture_score, final]
