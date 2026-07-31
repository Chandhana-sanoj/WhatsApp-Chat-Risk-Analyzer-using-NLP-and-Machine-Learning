# Module for parsing exported WhatsApp chat text files.
# Features a robust, multi-pattern sequential parser to handle different export formats globally.

import re
import pandas as pd

# Multi-pattern regex array to match various date-time separators and formats
PATTERNS = [
    # Pattern 1: Android 12h/24h with dash separator: "27/05/23, 14:32 - Sender: Message" or "27/05/23, 2:32 PM - Sender: Message"
    re.compile(r"^(\d{1,4}[/\.-]\d{1,2}[/\.-]\d{2,4},\s\d{1,2}:\d{2}(?::\d{2})?(?:\s?[aApP][mM])?)\s-\s([^:]+):\s?(.*)$"),
    
    # Pattern 2: iOS bracketed date-time: "[27/05/2023, 14:32:05] Sender: Message" or "[27/05/23, 2:32:05 PM] Sender: Message"
    re.compile(r"^\[(\d{1,4}[/\.-]\d{1,2}[/\.-]\d{2,4},\s\d{1,2}:\d{2}(?::\d{2})?(?:\s?[aApP][mM])?)\]\s([^:]+):\s?(.*)$"),
    
    # Pattern 3: Unbracketed with colons (Windows / Web): "27/05/23, 14:32: Sender: Message"
    re.compile(r"^(\d{1,4}[/\.-]\d{1,2}[/\.-]\d{2,4},\s\d{1,2}:\d{2}(?::\d{2})?(?:\s?[aApP][mM])?):\s([^:]+):\s?(.*)$")
]

# System notification check patterns
SYSTEM_PATTERNS = [
    re.compile(r"^(\d{1,4}[/\.-]\d{1,2}[/\.-]\d{2,4},\s\d{1,2}:\d{2}(?::\d{2})?(?:\s?[aApP][mM])?)\s-\s(.*)$"),
    re.compile(r"^\[(\d{1,4}[/\.-]\d{1,2}[/\.-]\d{2,4},\s\d{1,2}:\d{2}(?::\d{2})?(?:\s?[aApP][mM])?)\]\s(.*)$")
]

# Separators pattern from your notebook
SEPARATOR_PATTERN = re.compile(r"^[─—-]{5,}$")

def parse_chat(file_content: str, person: str, chat_name: str) -> list:
    """
    Parses WhatsApp exported chat text and returns a list of message dicts.
    Tries multiple patterns sequentially for high formatting compatibility.
    
    Parameters:
        file_content (str): The raw text of the WhatsApp chat.
        person (str): Name of the person under investigation.
        chat_name (str): Contact chat name (filename stem).
        
    Returns:
        list: List of dictionaries matching the notebook's message structure.
    """
    lines = file_content.splitlines()
    messages = []
    current_message = None

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if line == "":
            continue

        # Skip separators (e.g. ────)
        if SEPARATOR_PATTERN.match(line):
            continue

        # Check for message match using sequential regex patterns
        matched = False
        for pattern in PATTERNS:
            match = pattern.match(line)
            if match:
                # Save previous message
                if current_message is not None:
                    messages.append(current_message)

                timestamp = match.group(1)
                sender = match.group(2).strip()
                message = match.group(3).strip()

                current_message = {
                    "Person": person,
                    "Chat_Name": chat_name,
                    "Timestamp": timestamp,
                    "Sender": sender,
                    "Message": message
                }
                matched = True
                break
        
        if matched:
            continue
            
        # Check if it is a system event to clean/ignore it cleanly
        sys_matched = False
        for sys_pattern in SYSTEM_PATTERNS:
            sys_match = sys_pattern.match(line)
            if sys_match:
                if current_message is not None:
                    messages.append(current_message)
                timestamp = sys_match.group(1)
                sys_msg = sys_match.group(2).strip()
                
                # We skip standard encryption notices
                if "messages and calls are end-to-end encrypted" not in sys_msg.lower():
                    current_message = {
                        "Person": person,
                        "Chat_Name": chat_name,
                        "Timestamp": timestamp,
                        "Sender": "System Notification",
                        "Message": sys_msg
                    }
                else:
                    current_message = None
                sys_matched = True
                break
                
        if sys_matched:
            continue

        # Continuation of previous message
        if current_message is not None:
            current_message["Message"] += "\n" + line

    # Save last message
    if current_message is not None:
        messages.append(current_message)

    return messages


