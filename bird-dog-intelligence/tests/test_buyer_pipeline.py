import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("buyer_pipeline",ROOT/"buyer_pipeline.py")
m=importlib.util.module_from_spec(s)
s.loader.exec_module(m)

class BuyerDiscoveryTests(unittest.TestCase):
    def test_four_official_routes(self):
        self.assertEqual(len(m.validated_routes()),4)
        for x in m.validated_routes():
            self.assertEqual(x["partner_status"],"published_programme_only")
            self.assertTrue(x["official_page"].startswith("https://"))
    def test_discovery_plan_is_only_queries(self):
        self.assertEqual(len(m.discovery_plan(3)),3)
        self.assertTrue(all(x["status"]=="unexecuted_search" for x in m.discovery_plan(3)))
    def test_brief_is_not_send(self):
        a=m.brief("semibold")
        self.assertTrue(a["human_review_required"])
        self.assertTrue(a["no_outreach_sent"])
        self.assertIn("independently",a["draft_only_body"])

if __name__=="__main__":
    unittest.main()
