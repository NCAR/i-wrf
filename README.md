# I-WRF Repository Metrics

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
