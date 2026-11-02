"""Veille hebdomadaire : propositions GitHub Issues, publication seulement après 'oui'."""
import base64
import datetime as dt
import html
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo

import feedparser

ROOT = Path(__file__).resolve().parents[1]
REPO = os.environ.get("GITHUB_REPOSITORY", "")
TOKEN = os.environ.get("GH_TOKEN", "")
TZ = ZoneInfo("Europe/Paris")
FEEDS = {
    "cyber": [
        ("CERT-FR", "https://cert.cyber.gouv.fr/avis/feed/"),
        ("CERT-FR alertes", "https://cert.cyber.gouv.fr/alerte/feed/"),
        ("BleepingComputer", "https://www.bleepingcomputer.com/feed/"),
        ("The Hacker News", "https://feeds.feedburner.com/TheHackersNews"),
    ],
    "5g": [
        ("Google News — télécommunications", "https://news.google.com/rss/search?q=5G+OR+6G+OR+3GPP+OR+telecommunications+when%3A7d&hl=fr&gl=FR&ceid=FR%3Afr"),
        ("Google News — ARCEP et ANFR", "https://news.google.com/rss/search?q=site%3Aarcep.fr+OR+site%3Aanfr.fr+5G+when%3A14d&hl=fr&gl=FR&ceid=FR%3Afr"),
    ],
}
KEYWORDS = {
    "cyber": ("vulnérab", "sécurit", "cyber", "ransomware", "phishing", "malware", "breach", "attack", "exploit", "security", "zero-day", "pirat", "faille"),
    "5g": ("5g", "6g", "3gpp", "antenne", "réseau mobile", "telecom", "télécom", "satellite", "arcep", "anfr", "imt-2030"),
}
FILES = {
    "cyber": (ROOT / "data/cyber-articles.json", ROOT / "veille-cyber.html", "Cybersécurité", "assets/images/veille/veille-cyber.svg"),
    "5g": (ROOT / "data/5g-6g-articles.json", ROOT / "veille-5g-6g.html", "5G / 6G", "assets/images/veille/veille-5g.svg"),
}
STATE = ROOT / "data/veille-publications.json"
MARKER = re.compile(r"<!-- veille-proposition:([A-Za-z0-9_-]+) -->")
EMBED = re.compile(r'(<script\s+id="veilleData"\s+type="application/json">)(.*?)(</script>)', re.S)


def now():
    return dt.datetime.now(TZ)


def week():
    return now().strftime("%G-W%V")


def clean(text):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]*>", " ", str(text or "")))).strip()


def api(method, path, payload=None):
    if not (REPO and TOKEN):
        raise RuntimeError("GITHUB_REPOSITORY et GH_TOKEN sont requis")
    request = urllib.request.Request(
        "https://api.github.com/repos/" + REPO + path,
        data=None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "portfolio-veille"},
        method=method,
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response) if response.status != 204 else {}


def data_for(theme):
    return json.loads(FILES[theme][0].read_text(encoding="utf-8"))


def norm_url(url):
    parsed = urllib.parse.urlsplit(url.strip())
    return urllib.parse.urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(),
                                    parsed.path.rstrip("/"), "", ""))


def all_existing():
    return {norm_url(a.get("url", "")) for theme in FILES
            for a in data_for(theme).get("articles", []) if a.get("url")}


def parse_date(entry):
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed:
        return dt.date(*parsed[:3])
    return now().date()


def find_articles(theme):
    existing = all_existing()
    found = {}
    for source, feed_url in FEEDS[theme]:
        feed = feedparser.parse(feed_url, request_headers={"User-Agent": "PortfolioVeille/1.0"})
        if getattr(feed, "bozo", False) and not feed.entries:
            print("Flux inaccessible :", source, str(feed.get("bozo_exception", "")))
        for entry in feed.entries:
            url = entry.get("link", "").strip()
            title = clean(entry.get("title", ""))
            summary = clean(entry.get("summary", ""))[:450]
            date = parse_date(entry)
            key = norm_url(url)
            if not key or not url.startswith("https://") or key in existing or key in found:
                continue
            if not any(word in (title + " " + summary).lower() for word in KEYWORDS[theme]):
                continue
            if not (now().date() - dt.timedelta(days=21) <= date <= now().date()):
                continue
            found[key] = {"date": date.isoformat(), "category": "Actualités" if theme == "cyber" else "Réseaux mobiles",
                          "title": title, "source": source, "url": url, "summary": summary or title}
    return sorted(found.values(), key=lambda a: a["date"], reverse=True)[:3]


def make_token(theme, item, current_week):
    raw = json.dumps({"theme": theme, "week": current_week, "article": item}, ensure_ascii=False).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def read_token(body):
    match = MARKER.search(body or "")
    if not match:
        raise ValueError("Pas une proposition de veille")
    token = match.group(1)
    return json.loads(base64.urlsafe_b64decode(token + "=" * (-len(token) % 4)))


def issue_list():
    return api("GET", "/issues?state=all&per_page=100&sort=created&direction=desc")


def propose():
    current_week = week()
    previous = issue_list()
    existing = all_existing()
    for issue in previous:
        match = MARKER.search(issue.get("body") or "")
        if match:
            try:
                existing.add(norm_url(read_token(issue["body"])["article"]["url"]))
            except (ValueError, KeyError):
                pass
    for theme in FILES:
        if published(theme, current_week):
            continue
        candidates = [a for a in find_articles(theme) if norm_url(a["url"]) not in existing]
        for idx, item in enumerate(candidates, 1):
            token = make_token(theme, item, current_week)
            body = (
                "## Proposition de veille — " + FILES[theme][2] + "\n\n"
                + "**Semaine :** " + current_week + "\n\n"
                + "**Titre :** " + item["title"] + "\n\n"
                + "**Source :** " + item["source"] + " — " + item["date"] + "\n\n"
                + "**Article :** " + item["url"] + "\n\n"
                + "**Résumé du flux (à vérifier et corriger avant publication) :** " + item["summary"] + "\n\n"
                + "**Image :** illustration SVG originale du portfolio, non photo d'actualité.\n\n"
                + "### Pour décider\n"
                + "- Commente **oui** pour publier (maximum un article par thème et par semaine).\n"
                + "- Commente **non** pour refuser.\n"
                + "- Vérifie la source et le résumé : les flux peuvent être imprécis et ne sont pas forcément en français.\n\n"
                + "<!-- veille-proposition:" + token + " -->"
            )
            api("POST", "/issues", {"title": "[Veille " + theme.upper() + "] " + item["title"][:100],
                                     "body": body})
            existing.add(norm_url(item["url"]))
            print("Proposition créée :", theme, idx)


def published(theme, current_week):
    if not STATE.exists():
        return False
    state = json.loads(STATE.read_text(encoding="utf-8"))
    return bool(state.get(current_week, {}).get(theme))


def publish(theme, item, current_week):
    if published(theme, current_week):
        raise ValueError("Quota déjà atteint pour " + theme + " en " + current_week)
    docpath, pagepath, _, image_path = FILES[theme]
    doc = data_for(theme)
    if norm_url(item["url"]) in all_existing():
        raise ValueError("Article déjà publié")
    articles = doc.setdefault("articles", [])
    new_id = max((int(a.get("id", 0)) for a in articles), default=0) + 1
    article = dict(item, id=new_id, image=image_path,
                   image_prompt="Illustration originale générique — remplacer par une image vérifiée si souhaité.",
                   featured_text=item["title"][:140], approved_week=current_week)
    articles.insert(0, article)
    articles.sort(key=lambda a: a.get("date", ""), reverse=True)
    doc["updated"] = now().date().isoformat()
    page = pagepath.read_text(encoding="utf-8")
    raw = json.dumps(doc, ensure_ascii=False).replace("<", "\\u003c")
    page, count = EMBED.subn(lambda m: m.group(1) + raw + m.group(3), page, count=1)
    if count != 1:
        raise RuntimeError("Données veilleData introuvables dans " + str(pagepath))
    # S'assurer que le JSON et la page HTML contiennent la même liste publiée.
    json.loads(raw)
    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    state.setdefault(current_week, {})[theme] = {"url": item["url"], "published_at": now().isoformat()}
    docpath.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    pagepath.write_text(page, encoding="utf-8")
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def respond():
    number = int(os.environ["ISSUE_NUMBER"])
    response = os.environ.get("ISSUE_COMMENT", "").strip().lower()
    if response not in ("oui", "non"):
        print("Commentaire ignoré : répondre exactement oui ou non")
        return
    issue = api("GET", "/issues/" + str(number))
    if issue.get("state") != "open":
        return
    try:
        info = read_token(issue.get("body", ""))
    except (ValueError, KeyError):
        return
    theme = info["theme"]
    item = info["article"]
    current_week = info["week"]
    if theme not in FILES or not re.fullmatch(r"\d{4}-W\d{2}", current_week):
        raise ValueError("Métadonnées invalides")
    if response == "non":
        api("POST", "/issues/" + str(number) + "/comments",
            {"body": "❌ Proposition refusée. Aucun changement sur le portfolio."})
        api("PATCH", "/issues/" + str(number), {"state": "closed"})
        return
    if week() != current_week:
        api("POST", "/issues/" + str(number) + "/comments",
            {"body": "Cette proposition date d'une autre semaine. Relancer la recherche pour une proposition récente."})
        return
    if published(theme, current_week) or norm_url(item["url"]) in all_existing():
        api("POST", "/issues/" + str(number) + "/comments",
            {"body": "Publication refusée : quota de cette semaine déjà atteint ou article déjà publié."})
        return
    publish(theme, item, current_week)
    print("ARTICLE_APPROVED=" + theme)
    # Ne fermer la proposition qu’après la réussite du git push.
    output_path = os.environ.get("GITHUB_OUTPUT")
    if output_path:
        with open(output_path, "a", encoding="utf-8") as out:
            out.write("approved=true\\n".replace("\\n", "\n"))


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("propose", "respond"):
        raise SystemExit("Utilisation : python scripts/weekly_veille.py propose|respond")
    if sys.argv[1] == "propose":
        propose()
    else:
        respond()
