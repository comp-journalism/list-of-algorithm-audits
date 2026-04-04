#!/usr/bin/env python3
"""
Replace all instances of '2026 Refresh (Bandy)' with '2026 Refresh (Bandy)'.
Run with --apply to make changes; default is dry-run.
"""

import sys
import os
import glob

OLD = "2026 Refresh (Bandy)"
NEW = "2026 Refresh (Bandy)"
APPLY = "--apply" in sys.argv

EXTENSIONS = {".js", ".html", ".css", ".md", ".txt", ".csv", ".py", ".json"}

root = os.path.dirname(os.path.abspath(__file__))
total_files = 0
total_hits = 0

for dirpath, dirnames, filenames in os.walk(root):
    # Skip .git directory
    dirnames[:] = [d for d in dirnames if d != ".git"]
    for fname in filenames:
        if os.path.splitext(fname)[1] not in EXTENSIONS:
            continue
        fpath = os.path.join(dirpath, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
        except (UnicodeDecodeError, PermissionError):
            continue

        count = content.count(OLD)
        if count == 0:
            continue

        rel = os.path.relpath(fpath, root)
        total_files += 1
        total_hits += count

        for i, line in enumerate(content.splitlines(), 1):
            if OLD in line:
                print(f"  {rel}:{i}  {line.strip()}")

        if APPLY:
            new_content = content.replace(OLD, NEW)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"  → updated {rel} ({count} replacement{'s' if count > 1 else ''})")

print()
if total_hits == 0:
    print("No instances found.")
elif APPLY:
    print(f"Done. Replaced {total_hits} instance{'s' if total_hits > 1 else ''} across {total_files} file{'s' if total_files > 1 else ''}.")
else:
    print(f"Dry run: found {total_hits} instance{'s' if total_hits > 1 else ''} in {total_files} file{'s' if total_files > 1 else ''}. Run with --apply to replace.")
