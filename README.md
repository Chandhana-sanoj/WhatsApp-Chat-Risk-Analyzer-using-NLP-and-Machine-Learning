# AI WhatsApp Chat Risk Analyzer using NLP and Machine Learning

An AI-powered WhatsApp chat investigation system that analyzes exported WhatsApp conversations using Natural Language Processing (NLP) and Machine Learning to identify potentially suspicious messages and generate an interactive investigation dashboard.

> **Project Status:** Version 1 (Prototype)  
> This repository contains the first working version of the project. A more advanced Version 2 focused on domain-specific investigation and improved NLP techniques is currently under development.

---

## Project Overview

Investigating WhatsApp conversations manually becomes extremely difficult when thousands of messages are involved. This project automates the initial screening process by:

- Parsing exported WhatsApp chat files
- Cleaning and preprocessing message text
- Extracting textual features using TF-IDF
- Classifying messages using a Linear Support Vector Machine (Linear SVM)
- Aggregating message-level predictions into chat-level risk summaries
- Presenting the results through an interactive Streamlit dashboard

The system is designed as an **investigation support tool** that helps prioritize conversations for manual review. It does **not** determine criminal intent or replace human investigation.

---

## Features

- WhatsApp chat parser
- NLP-based text preprocessing
- TF-IDF feature extraction
- Linear SVM message classification
- Three-level risk prediction
  - Normal
  - Suspicious
  - High Risk
- Interactive Streamlit dashboard
- Chat-level risk ranking
- Risk distribution visualization
- Suspicious keyword analysis
- Activity timeline visualization
- Investigation summary generation

---

## Machine Learning Pipeline

```text
WhatsApp Chat Export (.txt)
            │
            ▼
WhatsApp Parser
            │
            ▼
Text Preprocessing
            │
            ▼
TF-IDF Vectorization
            │
            ▼
Linear SVM Classifier
            │
            ▼
Message Risk Prediction
            │
            ▼
Chat-Level Risk Aggregation
            │
            ▼
Interactive Dashboard
```

---

## Technologies Used

### Programming Language

- Python

### Machine Learning

- Scikit-learn
- Linear Support Vector Machine (Linear SVM)

### NLP

- NLTK
- TF-IDF Vectorizer
- Lemmatization
- Tokenization

### Data Processing

- Pandas
- NumPy

### Visualization

- Plotly
- Streamlit

### Model Storage

- Joblib

---

## Project Structure

```
AI_WhatsApp_Investigation_System/

├── app.py
├── parser.py
├── preprocess.py
├── predictor.py
├── styles.py
├── requirements.txt
├── README.md
│
├── models/
│   ├── best_message_classifier.pkl
│   └── best_tfidf_vectorizer.pkl
│
├── .streamlit/
│   └── config.toml
│
├── assets/
├── data/
└── reports/
```

---

## Dashboard

The Streamlit dashboard provides:

- Total Chats
- Total Messages
- Suspicious Message Count
- High Risk Chat Count
- Overall Risk Score
- Chat Risk Ranking
- Risk Distribution Chart
- Top Suspicious Keywords
- Suspicious Activity Timeline
- AI Investigation Summary

---

## Model Details

| Component | Method |
|----------|--------|
| Feature Extraction | TF-IDF |
| Classification Algorithm | Linear SVM |
| NLP Library | NLTK |
| Language | English (Primary) |
| Output Classes | Normal, Suspicious, High Risk |

---

## Current Limitations

This project represents the first prototype and has several known limitations.

- Message-level classification only
- Limited contextual understanding
- Does not analyze images, audio, or attachments
- Limited multilingual support
- WhatsApp system-generated messages require better filtering
- Small manually labeled dataset
- Rule-based aggregation for chat-level risk

---

## Future Improvements (Version 2)

The next version of this project will focus on **drug-related conversation investigation** rather than generic suspicious chat detection.

Planned improvements include:

- Domain-specific dataset for drug-related communication
- Improved annotation methodology
- Enhanced preprocessing for WhatsApp conversations
- Named Entity Recognition (NER)
- Context-aware message analysis
- Better risk scoring methodology
- Explainable AI (XAI) for prediction reasoning
- Automatic investigation report generation
- Improved dashboard and evidence visualization
- Better handling of code-mixed and multilingual conversations

---

## Research Motivation

The objective of this project is to demonstrate how Natural Language Processing and Machine Learning can assist investigators by reducing the manual effort required to screen large WhatsApp chat collections.

The system should be considered a **decision-support tool**, where flagged conversations are intended for further human review rather than automatic conclusions.

---

## License

This project is developed for academic and research purposes only.

The system is intended to assist investigation workflows and should not be used as the sole basis for legal or investigative decisions.
