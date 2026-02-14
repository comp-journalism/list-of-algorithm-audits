"""
Filter sample-1000-studies.csv to identify empirical algorithm audit studies.

An algorithm audit empirically tests/probes a deployed algorithmic system's behavior.
This script uses keyword/rule-based heuristics to filter conservatively (prefer
false positives over false negatives — the user will manually review output).
"""

import csv
import re
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(SCRIPT_DIR, "sample-1000-studies.csv")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "audits-from-sample.csv")

# --- Platforms / systems commonly audited ---
# Platforms as regex patterns to avoid false matches.
# Use word boundaries and case-sensitive matching where needed.
PLATFORMS = {
    "Google": r"\bGoogle\b",
    "Facebook": r"\bFacebook\b",
    "Amazon": r"\bAmazon\b",
    "YouTube": r"\bYouTube\b",
    "Twitter": r"\bTwitter\b",
    "TikTok": r"\bTikTok\b",
    "Instagram": r"\bInstagram\b",
    "LinkedIn": r"\bLinkedIn\b",
    "Spotify": r"\bSpotify\b",
    "Netflix": r"\bNetflix\b",
    "Uber": r"\bUber\b",
    "Lyft": r"\bLyft\b",
    "Airbnb": r"\bAirbnb\b",
    "Bing": r"\bBing\b",
    "Reddit": r"\bReddit\b",
    "Pinterest": r"\bPinterest\b",
    "Snapchat": r"\bSnapchat\b",
    "WhatsApp": r"\bWhatsApp\b",
    "Telegram": r"\bTelegram\b",
    "Alexa": r"\bAlexa\b",
    "Siri": r"\bSiri\b",
    "ChatGPT": r"\bChatGPT\b",
    "OpenAI": r"\bOpenAI\b",
    "GPT-4": r"\bGPT-4\b",
    "GPT-3": r"\bGPT-3\b",
    "DALL-E": r"\bDALL-E\b",
    "Midjourney": r"\bMidjourney\b",
    "Stable Diffusion": r"\bStable Diffusion\b",
    "Copilot": r"\bCopilot\b",
    "COMPAS": r"\bCOMPAS\b",
    "PredPol": r"\bPredPol\b",
    "Palantir": r"\bPalantir\b",
    "Clearview": r"\bClearview\b",
    "Rekognition": r"\bRekognition\b",
    "TaskRabbit": r"\bTaskRabbit\b",
    "Fiverr": r"\bFiverr\b",
    "Upwork": r"\bUpwork\b",
    "Booking.com": r"\bBooking\.com\b",
    "Hotels.com": r"\bHotels\.com\b",
    "Expedia": r"\bExpedia\b",
    "Orbitz": r"\bOrbitz\b",
    "Walmart": r"\bWalmart\b",
    "Zillow": r"\bZillow\b",
    "Redfin": r"\bRedfin\b",
    "Indeed": r"\bIndeed\.com\b",
    "Glassdoor": r"\bGlassdoor\b",
    "Craigslist": r"\bCraigslist\b",
    "eBay": r"\beBay\b",
    "Etsy": r"\bEtsy\b",
    "DoorDash": r"\bDoorDash\b",
    "GrubHub": r"\bGrubHub\b",
    "Instacart": r"\bInstacart\b",
    "Waze": r"\bWaze\b",
    "Google Maps": r"\bGoogle Maps\b",
    "Google Search": r"\bGoogle Search\b",
    "Google Ads": r"\bGoogle Ads?\b",
    "Facebook Ads": r"\bFacebook Ads?\b",
}

# --- Inclusion signals: strong indicators of audit-style work ---
STRONG_INCLUSION = [
    r"\baudit\w*\b",
    r"\bsock[ -]?puppet",
    r"\bbot[ -]?accounts?\b",
    r"\bscrap(ed|ing|e)\b.*\b(results?|data|pages?|outputs?)\b",
    r"\bcrowdsourc(ed|ing)\b.*\b(data|users?|workers?)\b",
    r"\btested?\b.*\b(algorithm|platform|system)\b",
    r"\bprob(ed?|ing)\b.*\b(algorithm|system|platform|bias)\b",
    r"\bblack[ -]?box\b.*\b(test|experiment|audit|analys)",
    r"\breverse[ -]?engineer",
]

MODERATE_INCLUSION = [
    r"\baudit\b",
    r"\bscrap(ed|ing|er?)\b",
    r"\bcrawl(ed|ing|er)\b",
    r"\bAPI\b.*\bcollect",
    r"\bcollect(ed|ing)\b.*\bAPI\b",
    r"\bexperiment\w*\b.*\b(platform|online|web|search|ad|recommend)",
    r"\b(platform|online|web|search|ad|recommend)\w*.*\bexperiment",
    r"\bbias\b.*\b(search|ad|recommend|rank|pric|hiring|recruit|crim|recidiv|lend|loan|credit)",
    r"\b(search|ad|recommend|rank|pric|hiring|recruit|crim|recidiv|lend|loan|credit)\w*.*\bbias\b",
    r"\bdiscrimination\b.*\b(algorithm|automat|online|platform|system)",
    r"\b(algorithm|automat|online|platform|system)\w*.*\bdiscrimination\b",
    r"\bfairness\b.*\b(search|ad|recommend|rank|pric|hiring|recruit|crim|recidiv|lend|loan|credit)",
    r"\balgorithm\w*\b.*\b(accountab|transparen|bias|fairness|discriminat|audit)",
    r"\b(accountab|transparen|bias|fairness|discriminat|audit)\w*.*\balgorithm",
    r"\bfilter[ -]?bubble",
    r"\becho[ -]?chamber",
    r"\bpersonaliz(ed|ation)\b.*\b(search|news|ad|recommend|price)",
    r"\bprice\b.*\b(discriminat|steer|personaliz|differentiat)",
    r"\bad\b.*\b(target|discriminat|bias|deliver)",
    r"\bcontent\b.*\b(moderat|remov|censor|suppress)",
    r"\bshadow[ -]?ban",
    r"\bde-?platform",
]

# Platform + action combo
PLATFORM_ACTIONS = [
    r"\btested?\b", r"\bexamin\w+\b", r"\banalyz\w+\b", r"\binvestigat\w+\b",
    r"\bmeasur\w+\b", r"\bevaluat\w+\b", r"\bstudi(ed|es)\b", r"\bscrap\w+\b",
    r"\bcrawl\w+\b", r"\bcollect\w+\b", r"\bquer(y|ied|ies)\b",
]

# --- Exclusion signals ---
STRONG_EXCLUSION = [
    r"\bsystematic (review|literature|mapping)\b",
    r"\bliterature review\b",
    r"\bmeta[ -]?analysis\b",
    r"\bsurvey of (the |existing |current |recent )?(literature|research|studies|work|approaches|methods)\b",
    r"\bscoping review\b",
    r"\bposition paper\b",
    r"\bcommentary\b",
    r"\beditorial\b",
    r"\btutorial\b",
    r"\bwe propose a (new |novel )?(framework|model|algorithm|method|approach|technique|system|architecture)\b",
    r"\bwe (introduce|present|develop) a (new |novel )?(framework|model|algorithm|method|approach|technique|system|architecture)\b",
    r"\bwe (design|build|implement) a (new |novel )?(framework|model|algorithm|method|approach|technique|system|architecture)\b",
    r"\bnovel (framework|model|algorithm|method|approach|technique|architecture)\b",
    r"\bperception(s)? of algorithm\b",
    r"\battitude(s)? toward(s)? algorithm\b",
    r"\buser (perception|attitude|experience|trust|acceptance)\b.*\balgorithm\b",
    r"\bhow (users?|people|individuals?) (perceive|experience|understand|feel about)\b",
    r"\binterview(s|ed)?\b.*\b(participant|user|respondent|stakeholder)\b",
    r"\bfocus group\b",
    r"\bthematic analysis\b.*\binterview\b",
]

MODERATE_EXCLUSION = [
    r"\bpropos(e|ed|ing) a\b",
    r"\btheoretical (framework|model|analysis|contribution)\b",
    r"\bnormative (framework|analysis|argument)\b",
    r"\bethical (framework|analysis|implication|consideration)\b",
    r"\bregulat(ion|ory) (framework|analysis|implication)\b",
    r"\bpolicy (framework|analysis|implication|recommendation)\b",
    r"\bsimulat(ed|ion)\b",
    r"\bsynthetic (data|dataset)\b",
    r"\bfinancial audit\b",
    r"\baudit (risk|judgment|opinion|report|quality|committee|firm|partner|profession)\b",
    r"\b(internal|external) audit\w*\b",
    r"\baccounting\b",
    r"\bauditor\b",
]


def text_matches(text, patterns):
    """Return number of pattern matches in text."""
    count = 0
    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            count += 1
    return count


def get_platform_mentions(text):
    """Return set of platform names found in text."""
    found = set()
    for name, pattern in PLATFORMS.items():
        if re.search(pattern, text):
            found.add(name)
    return found


def has_platform_mention(text):
    """Check if text mentions a known platform."""
    return len(get_platform_mentions(text)) > 0


def has_platform_action(text):
    """Check if text has a platform mention combined with an action word."""
    if not has_platform_mention(text):
        return False
    for action in PLATFORM_ACTIONS:
        if re.search(action, text, re.IGNORECASE):
            return True
    return False


def classify_study(title, abstract, keywords):
    """
    Classify whether a study is an empirical algorithm audit.
    Returns (is_audit: bool, confidence: str).
    """
    full_text = f"{title} {abstract} {keywords}"

    # Score exclusion signals
    strong_excl = text_matches(full_text, STRONG_EXCLUSION)
    moderate_excl = text_matches(full_text, MODERATE_EXCLUSION)

    # Score inclusion signals
    strong_incl = text_matches(full_text, STRONG_INCLUSION)
    moderate_incl = text_matches(full_text, MODERATE_INCLUSION)
    platform = has_platform_mention(full_text)
    platform_action = has_platform_action(full_text)

    # Check for empirical evidence signals — the study must show signs of
    # actually collecting data from or testing a real system
    empirical_signals = [
        r"\bcollect(ed|ing) data\b",
        r"\bdata(set)? (of|from|contain|consist|compris)",
        r"\b\d[\d,]* (tweets?|posts?|ads?|search|results?|profiles?|listings?|reviews?|videos?|images?|articles?|job|resum)\b",
        r"\bscrap(ed|ing)\b",
        r"\bcrawl(ed|ing)\b",
        r"\bAPI\b",
        r"\bexperiment\w*\b",
        r"\bmeasur(ed|ing|ement)\b.*\b(bias|discriminat|fairness|disparit)",
        r"\b(bias|discriminat|fairness|disparit)\w*.*\bmeasur(ed|ing|ement)\b",
        r"\bquantif(y|ied|ies)\b",
        r"\bstat?istic(al|s)?\b.*\b(analys|test|signific)",
        r"\bsock[ -]?puppet",
        r"\bbot[ -]?account",
    ]
    has_empirical = text_matches(full_text, empirical_signals) >= 1

    # Decision logic
    # Strong exclusion with no strong inclusion -> exclude
    if strong_excl >= 1 and strong_incl == 0:
        return False, "excluded-strong"

    # Strong inclusion -> include (but need some empirical signal or platform)
    if strong_incl >= 2:
        return True, "high"
    if strong_incl >= 1 and (has_empirical or platform):
        return True, "high"
    if strong_incl >= 1 and moderate_excl == 0:
        return True, "medium"

    # Platform + action + moderate inclusion + empirical
    if platform_action and moderate_incl >= 2 and has_empirical:
        return True, "medium"

    # Platform + several moderate inclusion signals + empirical
    if platform and moderate_incl >= 3 and has_empirical and moderate_excl == 0:
        return True, "medium"

    # Many moderate inclusions with empirical evidence, platform, and no exclusion
    if moderate_incl >= 4 and has_empirical and platform and moderate_excl == 0 and strong_excl == 0:
        return True, "low"

    return False, "excluded"


def abbreviate_authors(authors_str):
    """Convert 'Smith, John; Doe, Jane; Lee, Bob' to 'Smith et al.' or 'Smith and Doe'."""
    if not authors_str or authors_str.strip() == "":
        return ""
    # Authors are semicolon-separated: "Last, First; Last, First"
    authors = [a.strip() for a in authors_str.split(";") if a.strip()]
    if not authors:
        return ""
    # Extract last names (first part before comma)
    last_names = []
    for a in authors:
        parts = a.split(",")
        last_names.append(parts[0].strip())
    if len(last_names) == 1:
        return last_names[0]
    elif len(last_names) == 2:
        return f"{last_names[0]} and {last_names[1]}"
    else:
        return f"{last_names[0]} et al."


def make_url(link, doi):
    """Construct URL from Link or DOI."""
    if link and link.strip():
        return link.strip()
    if doi and doi.strip():
        return f"https://doi.org/{doi.strip()}"
    return ""


def classify_method(abstract):
    """Classify audit method from abstract text."""
    text = abstract.lower()
    methods = []
    if re.search(r"sock[ -]?puppet|fake (account|profile|user)", text):
        methods.append("Sock puppets")
    if re.search(r"crowdsourc|recruited (users?|participants?|workers?)|mechanical turk|mturk|prolific", text):
        methods.append("Crowdsourcing")
    if re.search(r"scrap(ed|ing|er?)|crawl(ed|ing|er)|collected? data (from|via|through|using).*API|API.*collect|query|quer(ied|ies)|bot[ -]?account", text):
        methods.append("Direct scrape")
    if re.search(r"source code|open[ -]?source.*code|code (audit|review|inspection|analysis)|inspect(ed|ing)? (the )?code", text):
        methods.append("Code")
    if not methods:
        methods.append("Direct scrape")  # default for audit studies
    return "\n".join(methods)


def classify_domain(title, abstract, keywords):
    """Classify audit domain from text."""
    text = f"{title} {abstract} {keywords}".lower()
    domains = []
    domain_patterns = [
        ("Search", r"\bsearch (engine|result|ranking|query|algorithm)|web search|google search|bing search|information retrieval"),
        ("Advertising", r"\badvertis|ad (delivery|targeting|auction)|online ad|digital ad|facebook ad|google ad"),
        ("Pricing", r"\bpric(e|ing)|e-?commerce|dynamic pricing|price discrimination|price differentiation|price steer"),
        ("Recommendation", r"\brecommend(ation|er)|news feed|timeline|content (curation|ranking|suggestion)|filter bubble|echo chamber|spotify|netflix|youtube.*suggest"),
        ("Criminal Justice", r"\bcriminal|recidiv|predict(ive)? polic|risk (assessment|score)|sentenc|bail|parole|compas|predpol"),
        ("Content Moderation", r"\bcontent moderat|censor|shadow.?ban|de.?platform|content (remov|block|suppress|filter)|hate speech.*detect|toxicity.*detect"),
        ("Healthcare", r"\bhealth|medical|clinical|patient|diagnos|disease|hospital|treatment"),
        ("Hiring", r"\bhir(e|ing)|recruit|resume|job (ad|post|recommend|match)|employment|labor market|talent"),
        ("Credit/Lending", r"\bcredit|lend|loan|mortgage|financial|insurance|underwriting"),
        ("Housing", r"\bhousing|real estate|rent|zillow|airbnb|redfin"),
        ("Social Media", r"\bsocial media|twitter|facebook|instagram|tiktok|reddit|platform"),
        ("Image/Vision", r"\bfacial recogn|face detect|image (search|classif|recogn)|computer vision|deepfake"),
        ("Language/NLP", r"\blanguage model|chatbot|chat.?gpt|text generat|natural language|nlp|sentiment|translat"),
    ]
    for domain, pattern in domain_patterns:
        if re.search(pattern, text):
            domains.append(domain)
    if not domains:
        return "Other"
    return domains[0]  # return primary domain


def extract_organization(title, abstract):
    """Extract the platform/system being audited."""
    text = f"{title} {abstract}"
    found = get_platform_mentions(text)
    if found:
        # Return in a stable order
        return "\n".join(sorted(found))
    return ""


def classify_behavior(abstract):
    """Classify the behavior being studied."""
    text = abstract.lower()
    behaviors = []
    if re.search(r"discriminat|bias|race|racial|gender|sex|ethnic|disparit|inequal|unfair|stereotyp", text):
        behaviors.append("Discrimination")
    if re.search(r"distort|misinform|disinform|filter bubble|echo chamber|polariz|manipulat|mislead|fake news", text):
        behaviors.append("Distortion")
    if re.search(r"exploit|privacy|surveil|track|dark pattern|manipulat.*user|extract|predatory", text):
        behaviors.append("Exploitation")
    if re.search(r"misjudg|error|inaccura|incorrect|false (positive|negative)|wrong|mistake|fail(ure|ed)|unreliab", text):
        behaviors.append("Misjudgement")
    if not behaviors:
        return "Discrimination"  # most common in audit studies
    return "\n".join(behaviors)


def main():
    studies = []
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            studies.append(row)

    print(f"Read {len(studies)} studies from {INPUT_FILE}")

    audits = []
    for row in studies:
        title = row.get("Title", "")
        abstract = row.get("Abstract", "")
        author_kw = row.get("Author Keywords", "")
        index_kw = row.get("Index Keywords", "")
        keywords = f"{author_kw} {index_kw}"

        is_audit, confidence = classify_study(title, abstract, keywords)
        if is_audit:
            authors = row.get("Authors", "")
            year = row.get("Year", "")
            doi = row.get("DOI", "")
            link = row.get("Link", "")

            audit_row = {
                "Title": title,
                "Abbreviated Authors": abbreviate_authors(authors),
                "Published Year": year,
                "Publication": "",
                "URL": make_url(link, doi),
                "Method": classify_method(abstract),
                "Domain": classify_domain(title, abstract, keywords),
                "Organization": extract_organization(title, abstract),
                "Behavior": classify_behavior(abstract),
            }
            audits.append((audit_row, confidence))

    print(f"Identified {len(audits)} potential audits")
    for conf in ["high", "medium", "low"]:
        count = sum(1 for _, c in audits if c == conf)
        print(f"  {conf} confidence: {count}")

    # Write output
    fieldnames = [
        "Title", "Abbreviated Authors", "Published Year", "Publication",
        "URL", "Method", "Domain", "Organization", "Behavior",
    ]
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for audit_row, _ in audits:
            writer.writerow(audit_row)

    print(f"Wrote {len(audits)} audits to {OUTPUT_FILE}")

    # Print a few examples
    print("\n--- Sample entries ---")
    for audit_row, conf in audits[:5]:
        print(f"\n[{conf}] {audit_row['Title']}")
        print(f"  Authors: {audit_row['Abbreviated Authors']}, Year: {audit_row['Published Year']}")
        print(f"  Domain: {audit_row['Domain']}, Method: {audit_row['Method'].split(chr(10))[0]}")
        print(f"  Organization: {audit_row['Organization'].split(chr(10))[0]}")
        print(f"  Behavior: {audit_row['Behavior'].split(chr(10))[0]}")


if __name__ == "__main__":
    main()
