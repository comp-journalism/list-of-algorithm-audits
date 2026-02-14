"""
Merge audits-from-paper.csv into feb2026-audits-compiled.json.

For any DOI in the JSON that matches a URL in the CSV,
overwrite the JSON entry's fields with the CSV data
and set Source to "2021 Review".
"""

import csv
import json
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent

json_path = ROOT / "feb2026-audits-compiled.json"
csv_path = ROOT / "audits-from-paper.csv"

# --- Load CSV into a dict keyed by URL (normalized) ---
def normalize_doi(doi: str) -> str:
    """Normalize URL for matching: lowercase, decode percent-encoding,
    normalize dx.doi.org -> doi.org, strip trailing slashes/whitespace."""
    s = doi.strip().lower()
    s = unquote(s)                        # %2F -> /
    s = s.replace("dx.doi.org", "doi.org")  # dx.doi.org -> doi.org
    s = s.replace("http://", "https://")    # http -> https
    s = s.rstrip("/")
    return s

def extract_id_suffix(url: str) -> str:
    """Extract the trailing numeric/path ID from a URL for fuzzy matching.
    E.g. 'https://ojs.aaai.org/index.php/icwsm/article/view/14898' -> '14898'
         'https://doi.org/10.5555/3277203.3277240' -> '3277203.3277240'
    """
    parts = url.rstrip("/").rsplit("/", 1)
    return parts[-1] if len(parts) > 1 else ""

csv_rows = {}
with open(csv_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        url = normalize_doi(row["URL"])
        csv_rows[url] = row

print(f"Loaded {len(csv_rows)} entries from CSV")

# --- Load JSON ---
with open(json_path, encoding="utf-8") as f:
    audits = json.load(f)

print(f"Loaded {len(audits)} entries from JSON")

# --- Build a fallback index: map trailing ID to CSV row for fuzzy matching ---
csv_by_suffix = {}
for url, row in csv_rows.items():
    suffix = extract_id_suffix(url)
    if suffix:
        csv_by_suffix[suffix] = (url, row)

# --- Merge ---
def apply_csv(entry, row):
    entry["Title"] = row["Title"]
    entry["Authors"] = row["Abbreviated Authors"]
    entry["Year"] = row["Published Year"]
    entry["Method"] = row["Method"]
    entry["Domain"] = row["Domain"]
    entry["Organization"] = row["Organization"]
    entry["Behavior"] = row["Behavior"]
    entry["Source"] = "2021 Review"

matched = 0
matched_urls = set()
for entry in audits:
    doi = normalize_doi(entry.get("DOI", ""))
    if doi in csv_rows:
        apply_csv(entry, csv_rows[doi])
        matched_urls.add(doi)
        matched += 1
    else:
        # Fallback 1: match on trailing ID suffix
        suffix = extract_id_suffix(doi)
        if suffix and suffix in csv_by_suffix:
            csv_url, row = csv_by_suffix[suffix]
            if csv_url not in matched_urls:
                apply_csv(entry, row)
                matched_urls.add(csv_url)
                matched += 1
                continue
        # Fallback 2: check if any CSV suffix appears within the JSON DOI
        # Handles e.g. ojs.aaai.org/.../view/14898 matching doi.org/10.1609/icwsm.v11i1.14898
        for csv_suffix, (csv_url, row) in csv_by_suffix.items():
            if csv_suffix.isdigit() and len(csv_suffix) >= 4 and csv_suffix in doi:
                if csv_url not in matched_urls:
                    apply_csv(entry, row)
                    matched_urls.add(csv_url)
                    matched += 1
                    break

print(f"Matched and updated {matched} entries")
print(f"Unmatched CSV entries: {len(csv_rows) - len(matched_urls)}")

# Show which CSV entries didn't match anything in the JSON
unmatched_csv = [url for url in csv_rows if url not in matched_urls]
if unmatched_csv:
    print("\nCSV entries with no matching DOI in JSON:")
    for url in unmatched_csv:
        print(f"  {csv_rows[url]['Abbreviated Authors']} ({csv_rows[url]['Published Year']}) - {url}")

# --- Write back ---
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(audits, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"\nWrote updated JSON to {json_path}")
