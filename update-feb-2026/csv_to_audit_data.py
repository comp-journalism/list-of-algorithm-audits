#!/usr/bin/env python3
"""Convert 2024-table-urman-et-al.csv to the JSON format used in audit-data.js."""

import csv
import json

INPUT = "/Users/jackb/GitHub/list-of-algorithm-audits/update-feb-2026/2024-table-urman-et-al.csv"
OUTPUT = "/Users/jackb/GitHub/list-of-algorithm-audits/update-feb-2026/audit-data.js"

FIELDS = [
    "Reference", "Year", "Organization", "Behavior", "Specific Behavior",
    "Method", "Domain", "Language", "Country Studied", "Country of Researchers",
    "DOI", "Title", "Authors", "Source",
]

with open(INPUT, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

# Build list of dicts with only the expected fields, preserving order
data = [{k: row.get(k, "") for k in FIELDS} for row in rows]

js = "const DATA = " + json.dumps(data, indent=2, ensure_ascii=False) + ";\n"

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(js)

print(f"Wrote {len(data)} entries to {OUTPUT}")
