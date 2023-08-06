import pytest
import unittest

from hemnes.helpers.Options import Options
from hemnes.helpers.PageFetcher import PageFetcher
from hemnes.helpers import scrape
from math import isclose

class TestScrape(unittest.TestCase):

    def test_process_query_0_results_pages_0_products(self):
        pf = PageFetcher()
        results = scrape.process_query(pf, 'alksdjflksdflksdjfkljds')
        self.assertEqual(0, len(results))
        # PageFetcher needs to be closed manually here because it's normally closed in hemnes.py
        pf.close()
        
    def test_process_query_1_results_pages_2_products(self):
        pf = PageFetcher()
        results = scrape.process_query(pf, 'yellow dog')
        self.assertEqual(2, len(results))
        expected_names = ['GOSIG GOLDEN', 'GOSIG GOLDEN']
        expected_ids = ['701.327.90', '801.327.99']
        expected_prices = [19.99, 9.99]
        # skipping the rest assuming that if the above 3 are correct the rest were okay
        # - also, the functionality of finding the product fields is tested in isolate above
        for i in range(len(results)):
            self.assertEqual(expected_names[i], results[i].name)
            self.assertEqual(expected_ids[i], results[i].id_no)
            self.assertTrue(isclose(expected_prices[i], results[i].price))
        # PageFetcher needs to be closed manually here because it's normally closed in hemnes.py
        pf.close()

    def test_light_process_query_2_results_pages_58_products(self):
        pf = PageFetcher()
        results = scrape.process_query(pf, 'mat')
        self.assertEqual(58, len(results))
        # PageFetcher needs to be closed manually here because it's normally closed in hemnes.py
        pf.close()
