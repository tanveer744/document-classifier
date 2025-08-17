# Document Classifier & Metadata Extractor

A beginner-friendly project that classifies PDF documents (Invoices, Resumes, Research Papers) and extracts useful metadata.  
Perfect for learning **NLP, machine learning, and database integration** — and directly maps to industry job roles.

---

## 🚀 Features
- **Document Classification**  
  - Uses TF-IDF + Logistic Regression to classify PDFs as `invoice`, `resume`, or `paper`.  
- **Metadata Extraction**  
  - Resumes → name, email, phone number  
  - Invoices → total amount  
  - Papers → title, author(s)  
- **Storage**  
  - Results stored in an SQLite database (`docs.sqlite`).  
- **End-to-End Workflow**  
  - Input → Process → Classify → Extract Metadata → Store → Query with SQL.

---

## 🛠 Tech Stack
- Python 3.x  
- [PyPDF2](https://pypi.org/project/pypdf2/) for PDF text extraction  
- [scikit-learn](https://scikit-learn.org/) for TF-IDF + Logistic Regression  
- [spaCy](https://spacy.io/) for Named Entity Recognition  
- [SQLite](https://www.sqlite.org/) for structured storage  

---

## 📂 Project Structure
```
document-classifier/
├── main.py              # main pipeline
├── db.py                # database operations
├── model.joblib         # trained ML model
├── requirements.txt     # dependencies
├── data/               # sample PDFs
│   ├── invoice.pdf
│   ├── resume.pdf
│   └── paper.pdf
├── docs.sqlite         # SQLite database
└── README.md           # documentation
```


---

## ⚡ Quick Start

1. **Clone repo:**
   ```bash
   git clone https://github.com/<your-username>/document-classifier.git
   cd document-classifier
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the model:**
   ```bash
   python main.py --train
   ```

4. **Process documents:**
   ```bash
   python main.py --process
   ```

5. **Explore results:**
   ```bash
   sqlite3 docs.sqlite
   SELECT * FROM documents LIMIT 5;
   ```

---

## ✅ Example Output
```
[OK] Model trained and saved
[OK] data/invoice.pdf → invoice → {'total': '$1,250.00'}
[OK] data/resume.pdf → resume → {'name': 'John Doe', 'email': 'johndoe@gmail.com', 'phone': '+91-9876543210'}
[OK] data/paper.pdf → paper → {'title': 'Neural Networks for NLP', 'authors': 'Jane Smith'}
[SUCCESS] Results stored in docs.sqlite
```

---

## 📋 Usage Options

### Command Line Arguments
- `--train` - Train the classification model
- `--process` - Process all documents in the data folder
- No arguments - Interactive mode with usage instructions

### Database Schema
The SQLite database contains two main tables:
- **documents**: stores document paths, labels, and processing timestamps
- **metadata**: stores extracted key-value metadata for each document

---

## 🎯 Learning Outcomes
This project teaches:
- **Text Processing**: PDF extraction, cleaning, preprocessing
- **Machine Learning**: TF-IDF vectorization, classification algorithms
- **NLP**: Named Entity Recognition, regex pattern matching
- **Database Design**: SQLite integration, schema design
- **Software Engineering**: Modular code structure, error handling

---

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create a Pull Request

---

## 📄 License
This project is open source and available under the [MIT License](LICENSE).