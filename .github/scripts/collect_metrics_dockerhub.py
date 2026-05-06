#!/usr/bin/env python3

import sys
import os
import csv
from datetime import datetime
from pathlib import Path

import requests

# DockerHub repositories to gather metrics
DOCKERHUB_REPOSITORIES = (
    "ncar/iwrf",
    "ncar/iwrf-metplus",
    "ncar/iwrf-data",
)

try:
    METRICS_DIR = Path(os.environ["METRICS_DIR"])
except KeyError:
    print("ERROR: Must set METRICS_DIR environment variable.")
    sys.exit(1)

CSV_FILE = os.path.join(METRICS_DIR, "dockerhub", "pull_counts.csv")

def get_all_pull_counts():
    counts = {}
    for repo in DOCKERHUB_REPOSITORIES:
        counts[repo] = get_pull_count(repo)
    return counts

def get_pull_count(repo):
    url = f"https://hub.docker.com/v2/repositories/{repo}/"
    response = requests.get(url)
    data = response.json()
    return data.get("pull_count", 0)

def update_csv(counts):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp"] + list(counts.keys()))
        writer.writerow([datetime.now().strftime("%Y-%m-%d")] + list(counts.values()))

if __name__ == "__main__":
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)
    count_dict = get_all_pull_counts()
    update_csv(count_dict)
    print(f"Updated {CSV_FILE} with pull counts: {count_dict}")
