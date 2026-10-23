"""No-network tests: python3 -m unittest discover -s tests -v"""
import importlib.util
import json
from pathlib import Path
import sys
import unittest

MODULE = Path(__file__).resolve().parents[1] / "run.py"
spec = importlib.util.spec_from_file_location("bird_dog_runner", MODULE)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class RegistryTests(unittest.TestCase):
    def test_manifest(self):
        self.assertGreaterEqual(mod.validate(), 15)
        sources = mod.read_json(mod.SRC)["sources"]
        self.assertTrue(all(s["url"].startswith("https://") for s in sources))
        self.assertEqual(len(set(x["id"] for x in sources)), len(sources))

    def test_planning_hard_filters(self):
        sources = mod.read_json(mod.SRC)["sources"]
        p = mod.tasks(sources, side="demand", limit=4)
        self.assertEqual(len(p), 4)
        self.assertTrue(all(x["side"] == "demand" for x in p))
        self.assertFalse(any(x["source_id"] == "uk_contracts_finder" for x in p))

    def test_tracking_removed(self):
        self.assertEqual(mod.canonical("https://example.com/rfp/?utm_source=z&x=1#top"),
                         "https://example.com/rfp?x=1")

    def test_no_internal_urls(self):
        for url in ("http://127.0.0.1:8000/", "http://localhost/x",
                    "https://10.0.0.2/", "file:///etc/passwd"):
            self.assertFalse(mod.safe_public_url(url))
        self.assertTrue(mod.safe_public_url("https://example.org/RFP"))

    def test_parse_decodo_search(self):
        sample = {"data": {"organic": [{"title": "Website RFP",
                                        "link": "https://example.org/rfp",
                                        "snippet": "Request for proposal deadline"}]}}
        results = mod.search_entries(sample)
        self.assertEqual(len(results), 1)
        src = {"side": "demand", "source_id": "test", "origin": "https://google.com",
               "verticals": ["website"], "query": "RFP"}
        item = mod.normalize(results[0], src)
        self.assertEqual(item["verification_status"], "unverified_search_result")
        self.assertEqual(item["signal"], "direct_request_candidate")
        self.assertIsNone(item["budget"])

    def test_no_published_programme_mistaken_for_contract(self):
        buy = mod.read_json(mod.BUYERS)["buyers"]
        task = {"side": "demand", "verticals": ["website"],
                "source_id": "a", "origin": "https://www.google.com/", "query": "a"}
        item = mod.normalize({"title":"RFP","link":"https://example.org/new"}, task)
        partner = mod.matching_published_programmes(item, buy)
        self.assertGreaterEqual(len(partner), 1)
        self.assertTrue(all(x["status"] == "published_only_not_contractually_approved" for x in partner))


if __name__ == "__main__":
    unittest.main()
