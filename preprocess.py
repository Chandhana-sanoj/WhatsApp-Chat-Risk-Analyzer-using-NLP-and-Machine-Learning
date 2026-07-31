# Text cleaning and preprocessing module.
# Matches your notebook's exact text normalization and tokenization logic.

import re
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# --- Download NLTK datasets gracefully ---
nltk_packages = ["punkt", "wordnet", "omw-1.4", "punkt_tab"]
for package in nltk_packages:
    try:
        if package in ["punkt", "punkt_tab"]:
            nltk.data.find(f"tokenizers/{package}")
        else:
            nltk.data.find(f"corpora/{package}")
    except LookupError:
        nltk.download(package, quiet=True)

# Set up lemmatizer
lemmatizer = WordNetLemmatizer()

# Regex for standard emojis
emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"
    "\U0001F300-\U0001F5FF"
    "\U0001F680-\U0001F6FF"
    "\U0001F1E0-\U0001F1FF"
    "]+",
    flags=re.UNICODE
)

def preprocess_text(text: str) -> str:
    """
    Cleans raw message text. Matches your notebook cell logic exactly:
    - Lowercasing
    - Link removal
    - <media omitted> removal
    - Time-date stamp removal
    - Emoji replacement
    - Retain alphanumeric & Malayalam characters (\u0D00-\u0D7F)
    - Tokenization (word_tokenize)
    - Lemmatization (WordNetLemmatizer)
    """
    if not isinstance(text, str):
        return ""
        
    # Lowercase
    text = text.lower()
    
    # Remove hyperlinks
    text = re.sub(r"http\S+|www\S+", "", text)
    
    # Remove <media omitted>
    text = re.sub(r"<media omitted>", "", text, flags=re.IGNORECASE)
    
    # Remove timestamps: e.g. 28/05/26, 14:15
    text = re.sub(r"\d{1,2}/\d{1,2}/\d{2},?\s+\d{1,2}:\d{2}\s*(am|pm)?", "", text, flags=re.IGNORECASE)
    
    # Remove standard emojis
    text = emoji_pattern.sub("", text)
    
    # Retain ONLY alphanumeric characters and Malayalam Unicode characters
    text = re.sub(r"[^\w\s\u0D00-\u0D7F]", " ", text)
    
    # Consolidate spaces
    text = re.sub(r"\s+", " ", text).strip()
    
    if not text:
        return ""
        
    # Tokenization
    try:
        tokens = word_tokenize(text)
    except Exception:
        tokens = text.split()
        
    # Lemmatize words
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    # Join back into a space-separated string
    return " ".join(tokens)

def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalizes timestamps, extracts hour features, and processes message text.
    
    Parameters:
        df (pd.DataFrame): Dataframe with 'Timestamp' and 'Message'.
        
    Returns:
        pd.DataFrame: Cleaned dataframe with 'Hour' and 'Processed_Message' columns.
    """
    if df.empty:
        df["Hour"] = []
        df["Processed_Message"] = []
        return df
        
    # Safe date conversion matching format: %d/%m/%y, %I:%M %p
    # e.g., "27/05/26, 09:12 AM" or "28/05/26, 10:00 AM"
    df["Timestamp_Parsed"] = pd.to_datetime(
        df["Timestamp"],
        format="%d/%m/%y, %I:%M %p",
        errors="coerce"
    )
    
    # Fill in missing dates if parsing failed
    df["Timestamp_Parsed"] = df["Timestamp_Parsed"].ffill().bfill()
    if df["Timestamp_Parsed"].isna().all():
        df["Timestamp_Parsed"] = pd.Timestamp.now()
        
    # Extract the hour feature (for the timeline line chart)
    df["Hour"] = df["Timestamp_Parsed"].dt.hour
    
    # Strip double whitespaces in the raw message column
    df["Message"] = (
        df["Message"]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )
    
    # Apply text cleaning
    df["Processed_Message"] = df["Message"].apply(preprocess_text)
    
    return df



