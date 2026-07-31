AI WhatsApp Chat Investigation System
A high-fidelity digital forensic investigation dashboard designed as a final year B.Tech machine learning project. The application analyzes exported WhatsApp chats, parses individual messages, cleans text content, and detects suspicious or high-risk communications using a trained TF-IDF Vectorizer and Linear Support Vector Machine (Linear SVM) Classifier.

📁 Project Structure

AI_WhatsApp_Investigation_System/
├── app.py                   # Main Streamlit web application (Screen 1 & Screen 2)
├── parser.py                # Regex-based WhatsApp chat log parser
├── preprocess.py            # Text cleaning and preprocessing module
├── predictor.py             # Model loading and risk scoring/prediction module
├── styles.py                # Injectable CSS styles and custom UI component functions
├── train_mock_models.py     # Helper script to create mock models for instant testing
├── requirements.txt         # Project package dependencies
│
├── .streamlit/
│   └── config.toml          # Custom theme settings (green forensic aesthetic)
│
├── models/                  # Destination folder for trained model pickle files
│   ├── best_tfidf_vectorizer.pkl
│   └── best_message_classifier.pkl
│
├── data/                    # Sample test chat data
│   └── test_chat.txt
│
├── assets/                  # Directory for UI images and icons
└── reports/                 # Directory for exporting investigation logs
🚀 Setup & Execution Instructions
Follow these steps to run the application on your local machine:

1. Install Dependencies
Open your command terminal, navigate to the project directory, and install the required packages:

bash

pip install -r requirements.txt
2. Prepare the Trained Models (Two Options)
The application expects your trained ML model files in the models/ directory:

models/best_tfidf_vectorizer.pkl
models/best_message_classifier.pkl
Option A: Use your actual trained model files
Move or copy your trained best_tfidf_vectorizer.pkl and best_message_classifier.pkl files directly into the models/ folder.

Option B: Generate mock model files for instant UI testing
If you do not have your final pickle files ready yet and want to explore the application flow, run the utility script to generate mock model files:

bash

python train_mock_models.py
This script fits a small vocabulary and trains a LinearSVC classifier on sample security phrases, saving the resulting .pkl files in the models/ folder.

3. Run the Streamlit Application
Launch the dev server using Streamlit:

bash

streamlit run app.py
This will open the application in your default web browser (usually at http://localhost:8501).

🔍 Testing with Sample Chat Data
We have provided a sample chat log to verify the system's capabilities:

When Screen 1 (Upload Page) opens, click the uploader box or drag-and-drop the file from data/test_chat.txt.
Click the Analyze Chat button.
Observe the step-by-step pipeline indicators:
Read Chat... ✔ Done
Parse Chat... ✔ Done
Preprocess... ✔ Done
Load TF-IDF... ✔ Done
Predict... ✔ Done
Generate Dashboard... ✔ Done
The system will automatically transition to Screen 2 (Dashboard), populating total chats, messages, risk distributions, suspicious keywords, and timelines dynamically based on the file content