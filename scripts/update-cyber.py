"""
AUTOMATISATION DE VEILLE CYBER
RSS -> Python -> JSON.
Installation : py -m pip install feedparser
Exécution : py scripts/update-cyber.py
Ce script est une démonstration d'automatisation : il récupère
les nouveautés et produit data/cyber-articles-auto.json.
"""
from pathlib import Path
from datetime import datetime
import json,re
try:
    import feedparser
except ImportError:
    raise SystemExit('Installe le module avec : py -m pip install feedparser')
ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'data'/'cyber-articles-auto.json'
FEEDS=[('BleepingComputer','https://www.bleepingcomputer.com/feed/'),('The Hacker News','https://feeds.feedburner.com/TheHackersNews')]
KEYWORDS={'cyber','security','ransomware','malware','phishing','vulnerability','exploit','breach','hack','zero-day','ai','agent','firewall','vpn','credential'}
def clean(v):return re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',v or '')).strip()
def main():
    articles=[];seen=set()
    for source,url in FEEDS:
        feed=feedparser.parse(url)
        for e in feed.entries:
            title=clean(e.get('title'));summary=clean(e.get('summary'));link=e.get('link','').strip()
            if not link or link in seen or not any(k in (title+' '+summary).lower() for k in KEYWORDS):continue
            seen.add(link);published=e.get('published_parsed');date=datetime(*published[:6]).strftime('%Y-%m-%d') if published else ''
            articles.append({'date':date,'category':'À classer','title':title,'source':source,'url':link,'summary':summary[:500]})
    articles.sort(key=lambda x:x['date'],reverse=True)
    OUTPUT.write_text(json.dumps({'updated':datetime.now().strftime('%Y-%m-%d'),'theme':'Cybersécurité - collecte automatique','articles':articles},ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{len(articles)} articles enregistrés dans {OUTPUT}')
if __name__=='__main__':main()
