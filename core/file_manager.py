import csv
import os

def load_csv(filename):
    """Load CSV file into a list of dictionaries."""
    if not os.path.exists(filename):
        return []
    with open(filename, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)

def save_csv(filename, data, fieldnames):
    """Save list of dictionaries to a CSV file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
