#!/usr/bin/env python3
"""Classify studies from sample-1000-studies.csv as algorithm audits or not,
using LM Studio (gemma-3n-e4b). Save audit studies to audits-from-feb12.csv."""

import csv
import json
import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

print_lock = threading.Lock()
WORKERS = 8  # concurrent requests to LM Studio

API_URL = "http://localhost:1234/v1/chat/completions"
MODEL = "google/gemma-3n-e4b"

# Ground truth examples for the prompt
AUDIT_EXAMPLES = """Examples of algorithm audit studies (INCLUDE these types):
- "Detecting price and search discrimination on the internet" - Tests whether websites show different prices to different users
- "Gender Shades: Intersectional Accuracy Disparities in Commercial Gender Classification" - Tests commercial facial recognition for bias
- "Auditing autocomplete: Suggestion networks and recursive algorithm interrogation" - Tests search autocomplete for bias
- "Algorithmic bias? An empirical study of apparent gender-based discrimination in the display of stem career ads" - Tests ad delivery for gender bias
- "Does Object Recognition Work for Everyone?" - Tests commercial object recognition across geographies

Examples of NON-audit studies (EXCLUDE these types):
- Systematic reviews or meta-analyses of existing literature
- Surveys of practitioners or users about their perceptions
- Position papers, opinion pieces, or commentaries
- Theoretical frameworks or taxonomies
- Papers about building/improving ML models without auditing deployed systems
- Papers about AI ethics, policy, or governance without empirical auditing
- Papers that study algorithmic bias conceptually but don't test a real system
- Papers that propose fairness metrics without applying them to audit a system
- Medical AI papers that evaluate model accuracy without a bias/fairness audit lens
- Papers about AI in education, healthcare etc. that don't audit for bias/discrimination"""

CLASSIFICATION_PROMPT = """You are classifying academic papers as algorithm audit studies or not.

An algorithm audit study is an EMPIRICAL study that tests, probes, or evaluates a deployed algorithmic system (like a search engine, recommendation system, ad platform, facial recognition API, pricing algorithm, etc.) for bias, discrimination, distortion, misjudgement, or exploitation. The study must involve actual data collection or experimentation with a real system.

{examples}

Based on the title, abstract, and keywords below, is this paper an algorithm audit study?

Title: {title}
Abstract: {abstract}
Author Keywords: {keywords}

Answer with ONLY "yes" or "no" (lowercase, nothing else)."""

EXTRACTION_PROMPT = """You are extracting structured information from an algorithm audit study.

The study audits an algorithmic system. Extract the following fields. Use the exact categories listed.

Method (pick one or more, newline-separated):
- Direct scrape (researchers directly query/test the system)
- Sock puppets (researchers create fake accounts/profiles to test)
- Carrier puppet (researchers use real accounts with modified attributes)
- Crowdsourcing (researchers recruit participants to test)
- Code (researchers analyze source code or open-source models)

Domain (pick one):
- Advertising, Criminal Justice, Language Processing, Mapping, Pricing, Recommendation, Search, Vision, Healthcare, Hiring, Social Media, Content Moderation, Credit/Finance, Other

Organization: The name(s) of the company/platform/system being audited (e.g., Google, Facebook, Amazon). Use newline to separate multiple. If unclear, leave blank.

Behavior (pick one):
- Discrimination (system treats groups differently based on protected attributes)
- Distortion (system presents skewed/inaccurate information)
- Exploitation (system takes advantage of users)
- Misjudgement (system makes systematic errors)

Title: {title}
Abstract: {abstract}
Author Keywords: {keywords}

Respond in EXACTLY this JSON format (no other text):
{{"method": "...", "domain": "...", "organization": "...", "behavior": "..."}}"""


def _call_llm(messages, max_tokens=10):
    """Call LM Studio API using urllib."""
    payload = json.dumps({
        "model": MODEL,
        "messages": messages,
        "temperature": 0.0,
        "max_tokens": max_tokens,
    }).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"].strip()


def classify_study(title, abstract, keywords):
    """Returns True if the study is classified as an algorithm audit."""
    prompt = CLASSIFICATION_PROMPT.format(
        examples=AUDIT_EXAMPLES,
        title=title,
        abstract=abstract[:2000] if abstract else "(no abstract)",
        keywords=keywords or "(none)"
    )
    try:
        answer = _call_llm([{"role": "user", "content": prompt}], max_tokens=10)
        return answer.lower().startswith("yes")
    except Exception as e:
        print(f"  [ERROR classifying] {e}", file=sys.stderr)
        return False


def extract_fields(title, abstract, keywords):
    """Extract Method, Domain, Organization, Behavior from an audit study."""
    prompt = EXTRACTION_PROMPT.format(
        title=title,
        abstract=abstract[:2000] if abstract else "(no abstract)",
        keywords=keywords or "(none)"
    )
    try:
        content = _call_llm([{"role": "user", "content": prompt}], max_tokens=200)
        start = content.find("{")
        end = content.rfind("}") + 1
        if start >= 0 and end > start:
            data = json.loads(content[start:end])
            return data
    except Exception as e:
        print(f"  [ERROR extracting] {e}", file=sys.stderr)
    return {"method": "", "domain": "", "organization": "", "behavior": ""}


def abbreviate_authors(authors_str):
    """Convert 'Smith, J.; Jones, B.; Lee, C.' to 'Smith et al.' or 'Smith and Jones'."""
    if not authors_str:
        return ""
    # Split by semicolons
    parts = [a.strip() for a in authors_str.split(";") if a.strip()]
    if not parts:
        return ""
    # Get last names
    last_names = []
    for p in parts:
        last = p.split(",")[0].strip()
        if last:
            last_names.append(last)
    if len(last_names) == 1:
        return last_names[0]
    elif len(last_names) == 2:
        return f"{last_names[0]} and {last_names[1]}"
    else:
        return f"{last_names[0]} et al."


def process_study(idx, total, study):
    """Classify a single study; return a row dict if it's an audit, else None."""
    title = study.get("Title", "")
    abstract = study.get("Abstract", "")
    keywords = study.get("Author Keywords", "")
    authors = study.get("Authors", "")
    year = study.get("Year", "")
    publication = study.get("Source title", "")
    url = study.get("Link", "")

    is_audit = classify_study(title, abstract, keywords)
    if not is_audit:
        with print_lock:
            print(f"[{idx+1}/{total}] NO  | {title[:80]}", flush=True)
        return None

    fields = extract_fields(title, abstract, keywords)
    row = {
        "Title": title,
        "Abbreviated Authors": abbreviate_authors(authors),
        "Published Year": year,
        "Publication": publication,
        "URL": url,
        "Method": fields.get("method", ""),
        "Domain": fields.get("domain", ""),
        "Organization": fields.get("organization", ""),
        "Behavior": fields.get("behavior", ""),
    }
    with print_lock:
        print(f"[{idx+1}/{total}] YES | {title[:60]} [{fields.get('domain','?')}]", flush=True)
    return row


def load_processed_titles(log_file):
    """Read classify_output.log and return set of already-processed titles."""
    processed = set()
    try:
        with open(log_file, encoding="utf-8") as f:
            for line in f:
                # Lines look like: [123/6554] YES | Title text...  or  [123/6554] NO  | Title text...
                if "] YES | " in line or "] NO  | " in line:
                    sep = "] YES | " if "] YES | " in line else "] NO  | "
                    title_part = line.split(sep, 1)[1].strip()
                    # YES lines have " [Domain]" suffix after truncated title
                    if sep == "] YES | " and " [" in title_part:
                        title_part = title_part[:title_part.rfind(" [")].strip()
                    processed.add(title_part)
    except FileNotFoundError:
        pass
    return processed


def main():
    input_file = "/Users/jackb/GitHub/list-of-algorithm-audits/update-feb-2026/all-studies-all-info-feb12.csv"
    output_file = "/Users/jackb/GitHub/list-of-algorithm-audits/update-feb-2026/audits-from-feb12.csv"
    log_file = "/Users/jackb/GitHub/list-of-algorithm-audits/update-feb-2026/classify_output.log"

    # Read all studies (file has BOM)
    with open(input_file, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        studies = list(reader)

    total = len(studies)

    # Load already-processed titles from log to support resuming
    processed_titles = load_processed_titles(log_file)
    already_done = 0
    remaining_studies = []
    for i, study in enumerate(studies):
        title = study.get("Title", "")
        # The log truncates titles: NO lines at 80 chars, YES lines at 60 chars
        # Check both truncation lengths
        if title[:80] in processed_titles or title[:60] in processed_titles:
            already_done += 1
        else:
            remaining_studies.append((i, study))

    print(f"Loaded {total} studies, {already_done} already processed, {len(remaining_studies)} remaining.")
    print(f"Resuming with {WORKERS} workers...")

    # Output columns matching audits-from-paper.csv
    fieldnames = ["Title", "Abbreviated Authors", "Published Year", "Publication", "URL", "Method", "Domain", "Organization", "Behavior"]

    audits_lock = threading.Lock()
    done = 0
    audit_count = 0

    # Append to CSV (write header only if file doesn't exist or is empty)
    import os
    csv_exists = os.path.exists(output_file) and os.path.getsize(output_file) > 0

    def append_audit_to_csv(row):
        nonlocal csv_exists
        with open(output_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if not csv_exists:
                writer.writeheader()
                csv_exists = True
            writer.writerow(row)

    with ThreadPoolExecutor(max_workers=WORKERS) as executor:
        futures = {
            executor.submit(process_study, i, total, study): i
            for i, study in remaining_studies
        }
        for future in as_completed(futures):
            done += 1
            result = future.result()
            if result is not None:
                with audits_lock:
                    audit_count += 1
                    append_audit_to_csv(result)

            if done % 100 == 0:
                print(f"  --- Progress: {done}/{len(remaining_studies)} processed, {audit_count} new audits found ---", flush=True)

    print(f"\nDone! Found {audit_count} new audit studies out of {len(remaining_studies)} remaining.")
    print(f"Appended to {output_file}")


if __name__ == "__main__":
    main()
