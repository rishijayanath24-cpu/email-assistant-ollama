"""Save Module: stores generated replies locally in a CSV file."""
import os
import pandas as pd

SAVE_PATH = "saved_replies/saved_replies.csv"
COLUMNS = ["Timestamp", "Customer Name", "Subject", "Email", "Intent", "Reply", "Tone"]


def save_reply(record: dict, path: str = SAVE_PATH) -> pd.DataFrame:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    row = pd.DataFrame([record], columns=COLUMNS)
    if os.path.exists(path):
        row = pd.concat([pd.read_csv(path), row], ignore_index=True)
    row.to_csv(path, index=False)
    return row


def load_saved(path: str = SAVE_PATH) -> pd.DataFrame:
    return pd.read_csv(path) if os.path.exists(path) else pd.DataFrame(columns=COLUMNS)
