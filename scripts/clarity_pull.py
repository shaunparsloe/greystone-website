#!/usr/bin/env python3
"""Daily pull of Microsoft Clarity dashboard data for greystoneguesthouse.co.za.

Reads CLARITY_API_TOKEN from ~/.config/greystone-seo/secrets.env and saves:
  analytics-data/clarity/raw/<YYYY-MM-DD>/<dimension>.json   raw API responses
  analytics-data/clarity/clarity_long.csv                    every value, one row each (for trends)
  analytics-data/clarity/pull_log.csv                        one row per run

Clarity allows 10 requests/project/day and only returns the last 1-3 days, so
this makes one request per dimension below (5 total) and, if the previous
successful pull was more than 24h ago, widens the window (max 3 days) to cover
the gap. Runs once per UTC day; re-running the same day does nothing.
"""
import csv
import json
import math
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://www.clarity.ms/export-data/api/v1/project-live-insights"
SECRETS = Path.home() / ".config/greystone-seo/secrets.env"
OUT = Path(__file__).resolve().parent.parent / "analytics-data/clarity"
# None = site-wide totals. Keep this list <= 5 to leave quota for ad-hoc queries.
DIMENSIONS = [None, "URL", "Device", "Channel", "Country/Region"]


def load_token():
    for line in SECRETS.read_text().splitlines():
        if line.startswith("CLARITY_API_TOKEN="):
            token = line.split("=", 1)[1].strip().strip('"').strip("'")
            if token:
                return token
    sys.exit(f"CLARITY_API_TOKEN is not set in {SECRETS}")


def last_success():
    log = OUT / "pull_log.csv"
    if not log.exists():
        return None
    rows = [r for r in csv.DictReader(log.open()) if r["status"] == "ok"]
    return datetime.fromisoformat(rows[-1]["pulled_at"]) if rows else None


def fetch(token, num_days, dimension):
    params = {"numOfDays": str(num_days)}
    if dimension:
        params["dimension1"] = dimension
    req = urllib.request.Request(
        f"{API}?{urllib.parse.urlencode(params)}",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp)


def flatten(data, pulled_at, num_days, dimension):
    """Yield one row per (metric, breakdown value, field)."""
    dim_key = dimension or ""
    for metric in data:
        for item in metric.get("information", []):
            dim_value = str(item.get(dimension, "")) if dimension else "(all)"
            for field, value in item.items():
                if field == dimension:
                    continue
                yield [pulled_at, num_days, dim_key, dim_value, metric.get("metricName", ""), field, value]


def main():
    now = datetime.now(timezone.utc).replace(microsecond=0)
    today = now.date().isoformat()
    prev = last_success()
    if prev and prev.date().isoformat() == today:
        print(f"Already pulled today ({prev.isoformat()}); nothing to do.")
        return

    hours = (now - prev).total_seconds() / 3600 if prev else 24
    num_days = max(1, min(3, math.ceil(hours / 24 - 0.05)))
    token = load_token()

    raw_dir = OUT / "raw" / today
    raw_dir.mkdir(parents=True, exist_ok=True)
    long_csv = OUT / "clarity_long.csv"
    new_file = not long_csv.exists()
    pulled_at = now.isoformat()
    status, done = "ok", 0

    with long_csv.open("a", newline="") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["pulled_at", "num_days", "dimension", "dimension_value", "metric", "field", "value"])
        for dim in DIMENSIONS:
            name = (dim or "totals").replace("/", "-").lower()
            try:
                data = fetch(token, num_days, dim)
            except urllib.error.HTTPError as e:
                status = f"http_{e.code}"
                print(f"{name}: HTTP {e.code} {e.reason}", file=sys.stderr)
                if e.code in (401, 403, 429):
                    break  # bad token or quota used up: further calls would fail too
                continue
            except urllib.error.URLError as e:
                status = "network_error"
                print(f"{name}: {e.reason}", file=sys.stderr)
                break
            (raw_dir / f"{name}.json").write_text(json.dumps(data, indent=2))
            w.writerows(flatten(data, pulled_at, num_days, dim))
            done += 1
            print(f"{name}: ok")

    log = OUT / "pull_log.csv"
    new_log = not log.exists()
    with log.open("a", newline="") as f:
        w = csv.writer(f)
        if new_log:
            w.writerow(["pulled_at", "num_days", "requests_ok", "status"])
        if status == "ok" and done < len(DIMENSIONS):
            status = "partial"
        w.writerow([pulled_at, num_days, done, status])
    if status != "ok":
        sys.exit(1)


if __name__ == "__main__":
    main()
