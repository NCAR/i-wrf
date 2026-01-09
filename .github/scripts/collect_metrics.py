#!/usr/bin/env python3
"""
Collect GitHub repository metrics for I-WRF.

This script collects traffic and repository statistics from the GitHub API
and stores them in CSV files for historical tracking. It uses the GitHub CLI
(gh) for authenticated API calls.

Usage:
    GH_TOKEN=<token> python collect_metrics.py

Requirements:
    - GitHub CLI (gh) installed and available in PATH
    - GH_TOKEN environment variable set with appropriate permissions
"""

import csv
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


# Configuration
REPO = os.environ.get("GITHUB_REPOSITORY", "NCAR/i-wrf")

# METRICS_DIR can be set via environment variable for flexible deployment
# Default: metrics/ directory relative to this script (for local testing)
if os.environ.get("METRICS_DIR"):
    METRICS_DIR = Path(os.environ["METRICS_DIR"])
else:
    METRICS_DIR = Path(__file__).parent.parent.parent / "metrics"

TRAFFIC_DIR = METRICS_DIR / "traffic"
REPOSITORY_DIR = METRICS_DIR / "repository"

# README content for the metrics branch
README_CONTENT = """# I-WRF Repository Metrics

This branch contains automatically collected usage metrics for the I-WRF repository.
Data is collected weekly via GitHub Actions and stored in CSV format for historical
analysis and reporting.

## Data Collection Schedule

- **Frequency:** Weekly (Sundays at 23:45 UTC)
- **Method:** GitHub Actions workflow using GitHub REST API
- **Workflow:** `.github/workflows/metrics-collection.yml` (on main branch)

## Why Weekly Collection?

GitHub only retains traffic data (views, clones) for **14 days**. The weekly schedule
ensures data is captured before it expires, with a safety margin allowing one missed
run before any data loss occurs.

## Directory Structure

```
metrics branch:
├── README.md              # This file
├── traffic/
│   ├── views.csv          # Daily page view counts
│   ├── clones.csv         # Daily repository clone counts
│   └── referrers.csv      # Top referral sources (weekly snapshots)
└── repository/
    ├── stats.csv          # Repository statistics over time
    └── summary.json       # Current state snapshot
```

## Data Schemas

### traffic/views.csv

| Column | Type | Description |
|--------|------|-------------|
| `date` | YYYY-MM-DD | Date of the recorded views |
| `views_total` | integer | Total page views that day |
| `views_unique` | integer | Unique visitors that day |
| `collection_timestamp` | ISO 8601 | When data was collected |

### traffic/clones.csv

| Column | Type | Description |
|--------|------|-------------|
| `date` | YYYY-MM-DD | Date of the recorded clones |
| `clones_total` | integer | Total git clones that day |
| `clones_unique` | integer | Unique cloners that day |
| `collection_timestamp` | ISO 8601 | When data was collected |

### traffic/referrers.csv

| Column | Type | Description |
|--------|------|-------------|
| `collection_date` | YYYY-MM-DD | Date of collection |
| `referrer` | string | Referring domain (e.g., google.com) |
| `count` | integer | Total visits from this referrer |
| `uniques` | integer | Unique visitors from this referrer |

### repository/stats.csv

| Column | Type | Description |
|--------|------|-------------|
| `date` | YYYY-MM-DD | Date of collection |
| `stars` | integer | Total stargazers |
| `forks` | integer | Total forks |
| `watchers` | integer | Total watchers |
| `open_issues` | integer | Currently open issues |
| `size_kb` | integer | Repository size in KB |

### repository/summary.json

Current state snapshot for programmatic access. Example:

```json
{
  "last_updated": "2024-01-07T23:45:00Z",
  "repository": {
    "stars": 48,
    "forks": 13,
    "watchers": 6,
    "open_issues": 2
  },
  "traffic_14_day_totals": {
    "views": 425,
    "views_unique": 112,
    "clones": 67,
    "clones_unique": 34
  }
}
```

## Using the Data

### Loading CSV Data (Python)

```python
import pandas as pd

views = pd.read_csv('traffic/views.csv', parse_dates=['date'])
clones = pd.read_csv('traffic/clones.csv', parse_dates=['date'])
stats = pd.read_csv('repository/stats.csv', parse_dates=['date'])

# Monthly summary
monthly_views = views.groupby(views['date'].dt.to_period('M')).agg({
    'views_total': 'sum',
    'views_unique': 'sum'
})
```

## Known Limitations

- **Traffic data accuracy:** GitHub notes that view and clone counts may have minor inaccuracies
- **14-day window:** Only the most recent 14 days of traffic data are available from the API
- **Referrer limits:** Only the top 10 referrers are returned per collection

## Data Gaps

If the collection workflow fails or is disabled, traffic data from that period is
permanently lost. Any known gaps will be documented here:

- *No gaps recorded*
"""


def gh_api(endpoint: str) -> dict:
    """
    Call GitHub API using gh CLI.

    Args:
        endpoint: API endpoint path (e.g., /repos/owner/repo/traffic/views)

    Returns:
        Parsed JSON response as dictionary

    Raises:
        subprocess.CalledProcessError: If API call fails
    """
    try:
        result = subprocess.run(
            ["gh", "api", endpoint],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error calling GitHub API {endpoint}: {e.stderr}", file=sys.stderr)
        raise


def ensure_directories():
    """Create metrics directories if they don't exist."""
    TRAFFIC_DIR.mkdir(parents=True, exist_ok=True)
    REPOSITORY_DIR.mkdir(parents=True, exist_ok=True)


def create_readme_if_missing():
    """Create README.md in metrics directory if it doesn't exist."""
    readme_path = METRICS_DIR / "README.md"
    if not readme_path.exists():
        print("Creating README.md...")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(README_CONTENT)
        print(f"  Created: {readme_path}")
    else:
        print(f"  README.md already exists: {readme_path}")


def read_existing_keys(filepath: Path, key_columns: list[str]) -> set[tuple]:
    """
    Read existing keys from a CSV file to support deduplication.

    Args:
        filepath: Path to CSV file
        key_columns: Column names that form the unique key

    Returns:
        Set of tuples representing existing keys
    """
    existing_keys = set()

    if filepath.exists() and filepath.stat().st_size > 0:
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = tuple(row.get(col, '') for col in key_columns)
                existing_keys.add(key)

    return existing_keys


def append_rows(filepath: Path, rows: list[dict], key_columns: list[str]) -> int:
    """
    Append rows to a CSV file, skipping duplicates based on key columns.

    Args:
        filepath: Path to CSV file
        rows: List of dictionaries to append
        key_columns: Column names that form the unique key

    Returns:
        Number of new rows added
    """
    if not rows:
        return 0

    existing_keys = read_existing_keys(filepath, key_columns)
    file_exists = filepath.exists() and filepath.stat().st_size > 0

    rows_added = 0
    fieldnames = list(rows[0].keys())

    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for row in rows:
            key = tuple(row.get(col, '') for col in key_columns)
            if key not in existing_keys:
                writer.writerow(row)
                existing_keys.add(key)
                rows_added += 1

    return rows_added


def collect_traffic_views(timestamp: str) -> list[dict]:
    """
    Collect page view traffic data.

    Args:
        timestamp: ISO format collection timestamp

    Returns:
        List of view records
    """
    print("Collecting traffic views...")
    data = gh_api(f"/repos/{REPO}/traffic/views")

    rows = []
    for view in data.get("views", []):
        # GitHub returns timestamps like "2024-01-01T00:00:00Z"
        date = view["timestamp"][:10]  # Extract YYYY-MM-DD
        rows.append({
            "date": date,
            "views_total": view["count"],
            "views_unique": view["uniques"],
            "collection_timestamp": timestamp
        })

    return rows


def collect_traffic_clones(timestamp: str) -> list[dict]:
    """
    Collect clone traffic data.

    Args:
        timestamp: ISO format collection timestamp

    Returns:
        List of clone records
    """
    print("Collecting traffic clones...")
    data = gh_api(f"/repos/{REPO}/traffic/clones")

    rows = []
    for clone in data.get("clones", []):
        date = clone["timestamp"][:10]
        rows.append({
            "date": date,
            "clones_total": clone["count"],
            "clones_unique": clone["uniques"],
            "collection_timestamp": timestamp
        })

    return rows


def collect_referrers(collection_date: str) -> list[dict]:
    """
    Collect top referrer data.

    Args:
        collection_date: Date of collection (YYYY-MM-DD)

    Returns:
        List of referrer records
    """
    print("Collecting referrers...")
    data = gh_api(f"/repos/{REPO}/traffic/popular/referrers")

    rows = []
    for referrer in data:
        rows.append({
            "collection_date": collection_date,
            "referrer": referrer["referrer"],
            "count": referrer["count"],
            "uniques": referrer["uniques"]
        })

    return rows


def collect_repository_stats(collection_date: str) -> dict:
    """
    Collect repository statistics.

    Args:
        collection_date: Date of collection (YYYY-MM-DD)

    Returns:
        Dictionary with repository stats
    """
    print("Collecting repository stats...")
    data = gh_api(f"/repos/{REPO}")

    return {
        "date": collection_date,
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "watchers": data.get("subscribers_count", 0),  # API uses subscribers_count for watchers
        "open_issues": data.get("open_issues_count", 0),
        "size_kb": data.get("size", 0)
    }


def generate_summary(timestamp: str, repo_stats: dict, views_data: list, clones_data: list):
    """
    Generate summary JSON file.

    Args:
        timestamp: ISO format timestamp
        repo_stats: Repository statistics dictionary
        views_data: List of view records from current collection
        clones_data: List of clone records from current collection
    """
    print("Generating summary...")

    # Calculate 14-day totals from current API response
    views_total = sum(v["views_total"] for v in views_data)
    views_unique = sum(v["views_unique"] for v in views_data)
    clones_total = sum(c["clones_total"] for c in clones_data)
    clones_unique = sum(c["clones_unique"] for c in clones_data)

    summary = {
        "last_updated": timestamp,
        "repository": {
            "stars": repo_stats["stars"],
            "forks": repo_stats["forks"],
            "watchers": repo_stats["watchers"],
            "open_issues": repo_stats["open_issues"]
        },
        "traffic_14_day_totals": {
            "views": views_total,
            "views_unique": views_unique,
            "clones": clones_total,
            "clones_unique": clones_unique
        }
    }

    summary_path = REPOSITORY_DIR / "summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print(f"  Written: {summary_path}")


def main():
    """Main entry point for metrics collection."""
    print(f"Starting metrics collection for {REPO}")
    print(f"Metrics directory: {METRICS_DIR}")

    # Get current timestamp
    now = datetime.now(timezone.utc)
    timestamp = now.isoformat()
    collection_date = now.strftime("%Y-%m-%d")

    print(f"Collection timestamp: {timestamp}")
    print()

    # Ensure directories exist and README is present
    ensure_directories()
    create_readme_if_missing()
    print()

    # Collect traffic views
    views_data = collect_traffic_views(timestamp)
    views_path = TRAFFIC_DIR / "views.csv"
    added = append_rows(views_path, views_data, ["date"])
    print(f"  Added {added} new view records to {views_path}")
    print()

    # Collect traffic clones
    clones_data = collect_traffic_clones(timestamp)
    clones_path = TRAFFIC_DIR / "clones.csv"
    added = append_rows(clones_path, clones_data, ["date"])
    print(f"  Added {added} new clone records to {clones_path}")
    print()

    # Collect referrers
    referrers_data = collect_referrers(collection_date)
    referrers_path = TRAFFIC_DIR / "referrers.csv"
    added = append_rows(referrers_path, referrers_data, ["collection_date", "referrer"])
    print(f"  Added {added} new referrer records to {referrers_path}")
    print()

    # Collect repository stats
    repo_stats = collect_repository_stats(collection_date)
    stats_path = REPOSITORY_DIR / "stats.csv"
    added = append_rows(stats_path, [repo_stats], ["date"])
    print(f"  Added {added} new stats record to {stats_path}")
    print()

    # Generate summary
    generate_summary(timestamp, repo_stats, views_data, clones_data)
    print()

    print("Metrics collection complete!")


if __name__ == "__main__":
    main()
