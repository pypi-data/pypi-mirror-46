import pytest
import unittest

from bs4 import BeautifulSoup
from hemnes.helpers import find_element
from hemnes.helpers import url_generator
from hemnes.helpers.Logger import Logger
from hemnes.helpers.Options import Options
from hemnes.helpers.PageFetcher import PageFetcher
from hemnes.helpers.Product import Product
from hemnes.helpers import scrape
from math import isclose
from shutil import rmtree
import os
import re

class TestUrlGenerator(unittest.TestCase):

    def test_get_url_for_search_results_single_word_page_1(self):
        query = 'chair'
        page_number = 1
        gen_url = url_generator.get_url_for_search_results(query, page_number)
        expected_url = 'https://www.ikea.com/ms/en_US/usearch/?&query=chair&rows=40&view=grid&start=0'
        self.assertEqual(expected_url, gen_url)

    def test_get_url_for_search_results_single_word_page_2(self):
        query = 'chair'
        page_number = 2
        gen_url = url_generator.get_url_for_search_results(query, page_number)
        expected_url = 'https://www.ikea.com/ms/en_US/usearch/?&query=chair&rows=40&view=grid&start=40'
        self.assertEqual(expected_url, gen_url)

    def test_get_url_for_search_results_single_word_page_25(self):
        query = 'chair'
        page_number = 25
        gen_url = url_generator.get_url_for_search_results(query, page_number)
        expected_url = 'https://www.ikea.com/ms/en_US/usearch/?&query=chair&rows=40&view=grid&start=960'
        self.assertEqual(expected_url, gen_url)        

    def test_get_url_for_search_results_multi_word_page_1(self):
        query = 'yellow chair'
        page_number = 1
        gen_url = url_generator.get_url_for_search_results(query, page_number)
        expected_url = 'https://www.ikea.com/ms/en_US/usearch/?&query=yellow+chair&rows=40&view=grid&start=0'
        self.assertEqual(expected_url, gen_url)

    def test_get_url_for_search_results_mutli_word_page_2(self):
        query = 'yellow chair'
        page_number = 2
        gen_url = url_generator.get_url_for_search_results(query, page_number)
        expected_url = 'https://www.ikea.com/ms/en_US/usearch/?&query=yellow+chair&rows=40&view=grid&start=40'
        self.assertEqual(expected_url, gen_url)

    def test_get_url_for_search_results_mutli_word_page_30(self):
        query = 'yellow chair'
        page_number = 30
        gen_url = url_generator.get_url_for_search_results(query, page_number)
        expected_url = 'https://www.ikea.com/ms/en_US/usearch/?&query=yellow+chair&rows=40&view=grid&start=1160'
        self.assertEqual(expected_url, gen_url)

    def test_get_url_for_search_results_mutli_word_multi_space_with_tab_literal_page_1(self):
        query = 'big\tyellow    \tchair'
        page_number = 1
        gen_url = url_generator.get_url_for_search_results(query, page_number)
        expected_url = 'https://www.ikea.com/ms/en_US/usearch/?&query=big+yellow+chair&rows=40&view=grid&start=0'
        self.assertEqual(expected_url, gen_url)

    def test_get_url_for_search_results_mutli_word_with_hyphen_with_tab_literal_page_1(self):
        query = 'big\tyellow-chair'
        page_number = 1
        gen_url = url_generator.get_url_for_search_results(query, page_number)
        expected_url = 'https://www.ikea.com/ms/en_US/usearch/?&query=big+yellow-chair&rows=40&view=grid&start=0'
        self.assertEqual(expected_url, gen_url)                        

class TestFindElement(unittest.TestCase):

    def setUp(self):
        # search results examples
        self.EXAMPLE_1_OF_15 = open('test/examples/results_1_of_15.html', 'r')
        self.EXAMPLE_1_OF_1 = open('test/examples/results_1_of_1.html', 'r')
        self.EXAMPLE_0_OF_0 = open('test/examples/results_0_of_0.html', 'r')
        
        self.SOUP_SEARCH_RESULTS_1_OF_15 = BeautifulSoup(self.EXAMPLE_1_OF_15.read(), 'html.parser')
        self.SOUP_SEARCH_RESULTS_1_OF_1 = BeautifulSoup(self.EXAMPLE_1_OF_1.read(), 'html.parser')
        self.SOUP_SEARCH_RESULTS_0_OF_0 = BeautifulSoup(self.EXAMPLE_0_OF_0.read(), 'html.parser')
        
        self.EXAMPLE_1_OF_15.close()
        self.EXAMPLE_1_OF_1.close()
        self.EXAMPLE_0_OF_0.close()

        # product page examples
        self.EXAMPLE_GUNDE = open('test/examples/product_page_GUNDE_60217799.html', 'r')
        self.EXAMPLE_VIMLE = open('test/examples/product_page_VIMLE_S19284744.html', 'r')
        self.EXAMPLE_MORBYLANGA_BERNHARD = open('test/examples/product_page_MÖRBYLÅNGA_BERNHARD_S69290139.html', 'r')
        self.EXAMPLE_SOMMAR = open('test/examples/product_page_SOMMAR_70419631.html')

        self.SOUP_GUNDE = BeautifulSoup(self.EXAMPLE_GUNDE.read(), 'html.parser')
        self.SOUP_VIMLE = BeautifulSoup(self.EXAMPLE_VIMLE.read(), 'html.parser')
        self.SOUP_MORBYLANGA_BERNHARD = BeautifulSoup(self.EXAMPLE_MORBYLANGA_BERNHARD.read(), 'html.parser')
        self.SOUP_SOMMAR = BeautifulSoup(self.EXAMPLE_SOMMAR.read(), 'html.parser')

        self.EXAMPLE_GUNDE.close()
        self.EXAMPLE_VIMLE.close()
        self.EXAMPLE_MORBYLANGA_BERNHARD.close()
        self.EXAMPLE_SOMMAR.close()

    def test_search_results_find_product_urls_40_results(self):
        product_urls = find_element.search_results_find_product_urls(self.SOUP_SEARCH_RESULTS_1_OF_15)
        self.assertTrue(len(product_urls) == 40)

    def test_search_results_find_product_urls_21_results(self):
        product_urls = find_element.search_results_find_product_urls(self.SOUP_SEARCH_RESULTS_1_OF_1)
        self.assertTrue(len(product_urls) == 21)

    def test_search_results_find_product_urls_0_results(self):
        product_urls = find_element.search_results_find_product_urls(self.SOUP_SEARCH_RESULTS_0_OF_0)
        self.assertTrue(len(product_urls) == 0)

    def test_product_page_find_product_name_gunde(self):
        name = find_element.product_page_find_product_name(self.SOUP_GUNDE)
        expected_name = 'GUNDE'
        self.assertEqual(expected_name, name)

    def test_product_page_find_product_name_vimle(self):
        name = find_element.product_page_find_product_name(self.SOUP_VIMLE)
        expected_name = 'VIMLE'
        self.assertEqual(expected_name, name)

    def test_product_page_find_product_name_with_slash_and_white_space_morbylanga_bernhard(self):
        name = find_element.product_page_find_product_name(self.SOUP_MORBYLANGA_BERNHARD)
        expected_name = 'MÖRBYLÅNGA BERNHARD'
        self.assertEqual(expected_name, name)

    def test_product_page_find_product_name_sommar(self):
        name = find_element.product_page_find_product_name(self.SOUP_SOMMAR)
        expected_name = 'SOMMAR 2019'
        self.assertEqual(expected_name, name)

    def test_product_page_find_product_id_gunde_602_177_99(self):
        prod_id = find_element.product_page_find_product_id(self.SOUP_GUNDE)
        expected_id = '602.177.99'
        self.assertEqual(expected_id, prod_id)

    def test_product_page_find_product_id_vimle_192_847_44(self):
        prod_id = find_element.product_page_find_product_id(self.SOUP_VIMLE)
        expected_id = '192.847.44'
        self.assertEqual(expected_id, prod_id)

    def test_product_page_find_product_id_morbylanga_bernhard_692_901_39(self):
        prod_id = find_element.product_page_find_product_id(self.SOUP_MORBYLANGA_BERNHARD)
        expected_id = '692.901.39'
        self.assertEqual(expected_id, prod_id)

    def test_product_page_find_product_id_sommar_704_196_31(self):
        prod_id = find_element.product_page_find_product_id(self.SOUP_SOMMAR)
        expected_id = '704.196.31'
        self.assertEqual(expected_id, prod_id)

    def test_product_page_find_product_price_gunde_7_99(self):
        price = find_element.product_page_find_product_price(self.SOUP_GUNDE)
        expected_price = 7.99
        self.assertTrue(isclose(expected_price, price))

    def test_product_page_find_product_price_vimle_649_00(self):
        price = find_element.product_page_find_product_price(self.SOUP_VIMLE)
        expected_price = 649.00
        self.assertTrue(isclose(expected_price, price))

    def test_product_page_find_product_price_morbylanga_bernhard_1135_00(self):
        price = find_element.product_page_find_product_price(self.SOUP_MORBYLANGA_BERNHARD)
        expected_price = 1135.00
        self.assertTrue(isclose(expected_price, price))

    def test_product_page_find_product_price_sommar_7_99(self):
        price = find_element.product_page_find_product_price(self.SOUP_SOMMAR)
        expected_price = 7.99
        self.assertTrue(isclose(expected_price, price))

    def test_product_page_find_product_rating_gunde_exists_4_4(self):
        rating = find_element.product_page_find_product_rating(self.SOUP_GUNDE)
        expected_rating = 4.4
        self.assertTrue(isclose(expected_rating, rating))

    def test_product_page_find_product_rating_vimle_no_reviews(self):
        rating = find_element.product_page_find_product_rating(self.SOUP_VIMLE)
        expected_rating = None
        self.assertEqual(expected_rating, rating)

    def test_product_page_find_product_rating_morbylanga_bernhard_no_reviews_2(self):
        rating = find_element.product_page_find_product_rating(self.SOUP_MORBYLANGA_BERNHARD)
        expected_rating = None
        self.assertEqual(expected_rating, rating)

    def test_product_page_find_product_rating_sommar_exists_5(self):
        rating = find_element.product_page_find_product_rating(self.SOUP_SOMMAR)
        expected_rating = 5
        self.assertEqual(expected_rating, rating)        

    def test_product_page_find_product_images_gunde_8(self):
        image_urls = find_element.product_page_find_product_images(self.SOUP_GUNDE)
        expected_num_of_images = 8
        expected_urls = [
            'https://www.ikea.com/PIAimages/0239249_PE378635_S3.JPG',
            'https://www.ikea.com/PIAimages/0750179_PH143072_S3.JPG',
            'https://www.ikea.com/PIAimages/0444896_PE595348_S3.JPG',
            'https://www.ikea.com/PIAimages/0445692_PE595993_S3.JPG',
            'https://www.ikea.com/PIAimages/0448925_PE598509_S3.JPG',
            'https://www.ikea.com/PIAimages/0437215_PE590754_S3.JPG',
            'https://www.ikea.com/PIAimages/0437020_PE590566_S3.JPG',
            'https://www.ikea.com/PIAimages/0437652_PE590987_S3.JPG'
        ]
        self.assertEqual(expected_num_of_images, len(image_urls))
        for i in range(len(image_urls)):
            self.assertEqual(expected_urls[i], image_urls[i])

    def test_product_page_find_product_images_vimle_6(self):
        image_urls = find_element.product_page_find_product_images(self.SOUP_VIMLE)
        expected_num_of_images = 7
        expected_urls = [
            'https://www.ikea.com/PIAimages/0514366_PE639439_S3.JPG',
            'https://www.ikea.com/PIAimages/0519609_PE641767_S3.JPG',
            'https://www.ikea.com/PIAimages/0519415_PE641673_S3.JPG',
            'https://www.ikea.com/PIAimages/0519418_PE641656_S3.JPG',
            'https://www.ikea.com/PIAimages/0519419_PE641657_S3.JPG',
            'https://www.ikea.com/PIAimages/0519417_PE641640_S3.JPG',
            'https://www.ikea.com/PIAimages/0743704_PE743114_S3.JPG'
        ]
        self.assertEqual(expected_num_of_images, len(image_urls))
        for i in range(len(image_urls)):
            self.assertEqual(expected_urls[i], image_urls[i])

    def test_product_page_find_product_images_morbylanga_bernhard_6(self):
        image_urls = find_element.product_page_find_product_images(self.SOUP_MORBYLANGA_BERNHARD)
        expected_num_of_images = 6
        expected_urls = [
            'https://www.ikea.com/PIAimages/0665848_PE713254_S3.JPG',
            'https://www.ikea.com/PIAimages/0665850_PE713256_S3.JPG',
            'https://www.ikea.com/PIAimages/0631802_PE695213_S3.JPG',
            'https://www.ikea.com/PIAimages/0436794_PE590379_S3.JPG',
            'https://www.ikea.com/PIAimages/0437019_PE590565_S3.JPG',
            'https://www.ikea.com/PIAimages/0437618_PE590953_S3.JPG'
        ]
        self.assertEqual(expected_num_of_images, len(image_urls))
        for i in range(len(image_urls)):
            self.assertEqual(expected_urls[i], image_urls[i])

    def test_product_page_find_product_images_sommar_no_thumb_1(self):
        image_urls = find_element.product_page_find_product_images(self.SOUP_SOMMAR)
        expected_num_of_images = 1
        expected_urls = [
            'https://www.ikea.com/us/en/images/products/sommar-bowl-with-lid-set-of-__0652948_PE707757_S4.JPG'
        ]
        self.assertEqual(expected_num_of_images, len(image_urls))
        for i in range(len(image_urls)):
            self.assertEqual(expected_urls[i], image_urls[i])

    def test_product_page_find_product_colors_gunde_1_white(self):
        colors = find_element.product_page_find_product_colors(self.SOUP_GUNDE)
        expected_num_of_colors = 1
        self.assertEqual(expected_num_of_colors, len(colors))
        expected_colors = {'white'}
        for i in range(len(colors)):
            self.assertTrue(colors[i] in expected_colors)
            expected_colors.remove(colors[i])

    def test_product_page_find_product_colors_vimle_1_beige(self):
        colors = find_element.product_page_find_product_colors(self.SOUP_VIMLE)
        expected_num_of_colors = 1
        self.assertEqual(expected_num_of_colors, len(colors))
        expected_colors = {'beige'}
        for i in range(len(colors)):
            self.assertTrue(colors[i] in expected_colors)
            expected_colors.remove(colors[i])

    def test_product_page_find_product_colors_morbylanga_bernhard_2_brown_blue(self):
        colors = find_element.product_page_find_product_colors(self.SOUP_MORBYLANGA_BERNHARD)
        expected_num_of_colors = 2
        self.assertEqual(expected_num_of_colors, len(colors))
        expected_colors = {'brown', 'blue'}
        for i in range(len(colors)):
            self.assertTrue(colors[i] in expected_colors)            

    def test_product_page_find_product_colors_sommar_0(self):
        colors = find_element.product_page_find_product_colors(self.SOUP_SOMMAR)
        self.assertEqual(None, colors)

    def test_product_page_has_keywords_gunde_strict_true(self):
        keywords = {'sturdy', 'backrest'}
        self.assertTrue(find_element.product_page_has_keywords(self.SOUP_GUNDE, keywords, strict=True))

    def test_product_page_has_keywords_gunde_strict_false(self):
        keywords = {'thisisntonthepage', 'neitheristhis', 'folding'}
        self.assertFalse(find_element.product_page_has_keywords(self.SOUP_GUNDE, keywords, strict=True))                       

    def test_product_page_has_keywords_gunde_not_strict_true(self):
        keywords = {'blueberries', 'unlikelywordtoappear', 'locks'}
        self.assertTrue(find_element.product_page_has_keywords(self.SOUP_GUNDE, keywords, strict=False))

    def test_product_page_has_keywords_gunde_not_strict_false(self):
        keywords = {'blueberries', 'unlikelywordtoappear', 'goldilocks'}
        self.assertFalse(find_element.product_page_has_keywords(self.SOUP_GUNDE, keywords, strict=False))

    def test_product_page_has_keywords_vimle_strict_true(self):
        keywords = {'regains', 'headrest', 'sofa'}
        self.assertTrue(find_element.product_page_has_keywords(self.SOUP_VIMLE, keywords, strict=True))

    def test_product_page_has_keywords_vimle_strict_false(self):
        keywords = {'thisisntonthepage', 'sofa', 'folding'}
        self.assertFalse(find_element.product_page_has_keywords(self.SOUP_VIMLE, keywords, strict=True))                       

    def test_product_page_has_keywords_vimle_not_strict_true(self):
        keywords = {'blueberries', 'warranty', 'locks'}
        self.assertTrue(find_element.product_page_has_keywords(self.SOUP_VIMLE, keywords, strict=False))

    def test_product_page_has_keywords_vimle_not_strict_false(self):
        keywords = {'blueberries', 'unlikelywordtoappear', 'goldilocks'}
        self.assertFalse(find_element.product_page_has_keywords(self.SOUP_VIMLE, keywords, strict=False))                
                        
class TestLogger(unittest.TestCase):

    def setUp(self):
        self.TEST_LOG_DIR = 'test/hemnes-logs'
        if(not os.path.exists(self.TEST_LOG_DIR)): os.mkdir(self.TEST_LOG_DIR)
        self.logger = Logger(log_dir=self.TEST_LOG_DIR, log_to_console=False)
        self.full_path = self.logger._Logger__full_path

    def tearDown(self):
        self.logger.close()
        # remove files made from test cases
        if os.path.exists(self.full_path):
            os.remove(self.full_path)
        if os.path.exists(self.TEST_LOG_DIR) and os.path.isdir(self.TEST_LOG_DIR):
            rmtree(self.TEST_LOG_DIR)

    def test_log_file_is_created_on_init(self):
        self.assertTrue(os.path.exists(self.full_path))

    def test_log_file_naming_convention_is_upheld(self):
        match_span = re.match(r'([A-Za-z0-9_-]*/)*hemnes(-\d{2,2}){3,3}(:\d{2,2}){2,2}\.log', self.full_path).span()
        self.assertEqual(match_span[0], 0)
        self.assertEqual(match_span[1], len(self.full_path))

class TestOptions(unittest.TestCase):

    def setUp(self):
        self.options = Options()

    def test_cdriver_path_str_no_raises(self):
        self.options.cdriver_path = 'this isnt a real path'

    def test_cdriver_path_int_raises(self):
        with self.assertRaises(ValueError):
            self.options.cdriver_path = 5

    def test_keywords_set_no_raises(self):
        self.options.keywords = set()

    def test_keywords_list_raises(self):
        with self.assertRaises(ValueError):
            self.options.keywords = []

    def test_log_bool_no_raises(self):
        self.options.log = True

    def test_log_int_raises(self):
        with self.assertRaises(ValueError):
            self.options.log = 1

    def test_num_results_int_no_raises(self):
        self.options.num_results = 5

    def test_num_results_float_raises(self):
        with self.assertRaises(ValueError):
            self.options.num_results = 5.5

    def test_sleep_time_int_no_raises(self):
        self.options.sleep_time = 4

    def test_sleep_time_float_raises(self):
        with self.assertRaises(ValueError):
            self.options.sleep_time = 4.5

    def test_sleep_time_negative_num_defaults_to_0(self):
        self.options.sleep_time = -1
        self.assertEqual(0, self.options.sleep_time)

    def test_strict_bool_no_raises(self):
        self.options.strict = True

    def test_strict_int_raises(self):
        with self.assertRaises(ValueError):
            self.options.strict = 0

    def test_tag_str_no_raises(self):
        self.options.tag = 'fake tag'

    def test_tag_int_raises(self):
        with self.assertRaises(ValueError):
            self.options.tag = 5

if __name__ == '__main__':
    unittest.main()
