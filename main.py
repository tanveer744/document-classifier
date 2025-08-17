import re
import sqlite3
import pandas as pd
from pathlib import Path
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from joblib import dump, load
import spacy

# --------- STEP 1: Extract PDF Text ----------
def extract_text(pdf_path):
    try:
        reader = PdfReader(str(pdf_path))
        return " ".join([p.extract_text() or "" for p in reader.pages])
    except Exception:
        return ""

# --------- STEP 2: Build Dataset ----------
def build_dataset():
    rows = []
    for pdf in Path("data").glob("*.pdf"):
        text = extract_text(pdf)
        # simple labeling by filename
        if "invoice" in pdf.name.lower():
            label = "invoice"
        elif "resume" in pdf.name.lower():
            label = "resume"
        else:
            label = "paper"
        rows.append([str(pdf), text, label])
    return pd.DataFrame(rows, columns=["path", "text", "label"])

# --------- STEP 3: Train Classifier ----------
def train(df):
    X, y = df["text"], df["label"]
    vec = TfidfVectorizer(stop_words="english", max_features=5000)
    Xv = vec.fit_transform(X)
    clf = LogisticRegression(max_iter=200)
    clf.fit(Xv, y)
    dump((vec, clf), "model.joblib")
    print("[OK] Model trained and saved")

# --------- STEP 4: Metadata Extractors ----------
nlp = spacy.load("en_core_web_sm")
EMAIL = re.compile(r"\S+@\S+")
PHONE = re.compile(r"\+?\d[\d\s\-]{7,}")
MONEY = re.compile(r"\$?\d+(?:\.\d{2})?")

def extract_metadata(label, text):
    if label == "resume":
        doc = nlp(text[:3000])
        name = next((ent.text for ent in doc.ents if ent.label_=="PERSON"), None)
        email = EMAIL.search(text)
        phone = PHONE.search(text)
        return {"name": name, "email": email.group() if email else None,
                "phone": phone.group() if phone else None}
    elif label == "invoice":
        amount = MONEY.search(text)
        return {"total": amount.group() if amount else None}
    elif label == "paper":
        first_lines = [l for l in text.split("\n") if l.strip()][:5]
        title = first_lines[0] if first_lines else None
        doc = nlp(" ".join(first_lines))
        authors = [ent.text for ent in doc.ents if ent.label_=="PERSON"]
        return {"title": title, "authors": ", ".join(authors)}
    return {}

# --------- STEP 5: Store in SQLite ----------
def store(df, vec, clf):
    con = sqlite3.connect("docs.sqlite")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS documents (path TEXT, label TEXT, meta TEXT)")
    
    for _, row in df.iterrows():
        Xv = vec.transform([row["text"]])
        pred = clf.predict(Xv)[0]
        meta = extract_metadata(pred, row["text"])
        cur.execute("INSERT INTO documents VALUES (?,?,?)", (row["path"], pred, str(meta)))
        print(f"[OK] {row['path']} → {pred} → {meta}")
    
    con.commit()
    con.close()
    print("[OK] Results stored in docs.sqlite")

# --------- MAIN PIPELINE ----------
if __name__ == "__main__":
    df = build_dataset()
    train(df)
    vec, clf = load("model.joblib")
    store(df, vec, clf)
