import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts/weekly_veille.py"
spec = importlib.util.spec_from_file_location("veille", MODULE_PATH)
veille = importlib.util.module_from_spec(spec)
spec.loader.exec_module(veille)


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "data").mkdir()
        self.doc = self.root / "data/articles.json"
        self.html = self.root / "veille.html"
        self.state = self.root / "data/veille-publications.json"
        self.original = {
            "updated": "2026-10-11",
            "theme": "5G / 6G",
            "articles": [{"id": 1, "date": "2026-10-01", "category": "5G",
                          "title": "Ancien article", "source": "Arcep",
                          "url": "https://example.org/ancien", "summary": "Ancien",
                          "image": "assets/images/veille/old.jpg"}],
        }
        self.doc.write_text(json.dumps(self.original), encoding="utf-8")
        self.html.write_text('<html><script id="veilleData" type="application/json">'
                             + json.dumps(self.original) + '</script></html>',
                             encoding="utf-8")
        self.files = {"5g": (self.doc, self.html, "5G/6G", "assets/images/veille/veille-5g.svg")}
        self.item = {
            "date": "2026-10-28",
            "category": "6G",
            "title": "L’ETSI travaille sur les communications 6G",
            "source": "ETSI",
            "url": "https://etsi.org/news/6g",
            "summary": "Une nouvelle norme 6G est à l’étude.",
        }
        self.p1 = patch.object(veille, "FILES", self.files)
        self.p2 = patch.object(veille, "STATE", self.state)
        self.p1.start()
        self.p2.start()

    def tearDown(self):
        self.p2.stop()
        self.p1.stop()
        self.tmp.cleanup()

    def test_publication_updates_json_and_html_without_deleting_old_articles(self):
        veille.publish("5g", self.item, "2026-W45")
        data = json.loads(self.doc.read_text(encoding="utf-8"))
        embedded = re.search(r'<script id="veilleData" type="application/json">(.*?)</script>',
                             self.html.read_text(encoding="utf-8"), re.S)
        self.assertIsNotNone(embedded)
        html_data = json.loads(embedded.group(1))
        self.assertEqual(len(data["articles"]), 2)
        self.assertEqual(data["articles"], html_data["articles"])
        self.assertEqual(data["articles"][0]["title"], self.item["title"])
        self.assertEqual(data["articles"][1]["title"], "Ancien article")
        self.assertEqual(data["articles"][0]["image"], "assets/images/veille/veille-5g.svg")
        self.assertTrue(veille.published("5g", "2026-W45"))

    def test_second_article_same_week_is_rejected(self):
        veille.publish("5g", self.item, "2026-W45")
        with self.assertRaisesRegex(ValueError, "Quota"):
            veille.publish("5g", {**self.item, "url": "https://etsi.org/news/other"}, "2026-W45")

    def test_duplicate_article_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "déjà publié"):
            veille.publish("5g", {**self.item, "url": "https://example.org/ancien"}, "2026-W45")


if __name__ == "__main__":
    unittest.main()
