# src/utils/log_helper.py
import os

LOG_FILE = "processed_log.txt"


def is_processed(name):
    if not os.path.exists(LOG_FILE):
        return False
    with open(LOG_FILE, "r") as f:
        processed = f.read().splitlines()
    return name in processed


def mark_as_processed(name):
    with open(LOG_FILE, "a") as f:
        f.write(f"{name}\n")
