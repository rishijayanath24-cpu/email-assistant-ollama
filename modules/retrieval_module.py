"""Retrieval Module: finds similar past emails with Sentence Transformers."""
import numpy as np
import pandas as pd

EMBED_MODEL = "all-MiniLM-L6-v2"


class SentenceTransformerEmbedder:
    def __init__(self, model_name: str = EMBED_MODEL):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        return self.model.encode(list(texts), normalize_embeddings=True)


class EmailRetriever:
    def __init__(self, csv_path: str = "data/past_emails.csv", embedder=None):
        self.df = pd.read_csv(csv_path)
        self.embedder = embedder or SentenceTransformerEmbedder()
        corpus = (self.df["Subject"] + ". " + self.df["Email"]).tolist()
        self.vectors = np.asarray(self.embedder.encode(corpus))

    def retrieve(self, subject: str, email: str, top_k: int = 3) -> pd.DataFrame:
        query = np.asarray(self.embedder.encode([f"{subject}. {email}"]))[0]
        scores = self.vectors @ query
        top = np.argsort(scores)[::-1][:top_k]
        result = self.df.iloc[top].copy()
        result["Similarity"] = np.round(scores[top], 3)
        return result.reset_index(drop=True)
