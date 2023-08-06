"""Main functionality for hemnes - ikea scraping"""

__author__ = 'sayeef moyen'

# import
from hemnes.helpers import Logger, Options, PageFetcher, Product, scrape
import csv
import json

def process_query(query, options=None):
    """Returns a list of products found for a query.

    Args:
        query (str): query words
        options (Options): Options object specifying extended requirements/actions

    Returns:
        list[Product]: Products found
    """
    ext_options = Options.Options() if options is None else options
    pf = PageFetcher.PageFetcher(chromedriver_path=ext_options.cdriver_path, sleep_time=ext_options.sleep_time)
    logger = None if not ext_options.log else Logger.Logger()
    # pass in the options
    results = scrape.process_query(pf, query, keywords=ext_options.keywords, logger=logger, num_desired=ext_options.num_results, strict=ext_options.strict, tag=ext_options.tag)
    pf.close()
    if logger is not None: logger.close()
    # writing to files
    json_dump_path = ext_options.json_dump
    csv_dump_path = ext_options.csv_dump
    try:
        if json_dump_path is not None or csv_dump_path is not None:
            # turn all of the Product objects into dictionaries before writing to json
            dict_results = [product.to_dict() for product in results]
            if json_dump_path is not None:
                with open(json_dump_path, 'w+') as json_dump:
                    json.dump(dict_results, json_dump, indent=4)
            if csv_dump_path is not None:
                fieldnames = ['name', 'id_no', 'price', 'url', 'rating', 'img_urls', 'colors', 'tag']
                with open(csv_dump_path, 'w+') as csv_dump:
                    writer = csv.DictWriter(csv_dump, fieldnames=fieldnames)
                    writer.writeheader()
                    for result in dict_results:
                        writer.writerow(result)
    except Exception:
        # avoid losing results due to IO issues
        if logger is not None:
            logger.log('ERROR: unexpected error when writing data to json/csv - returning %d results' % (len(results)))
    finally:
        return results

def speedtest():
    """Returns an estimate of the lowest viable sleep time for a network

    Returns:
        int: recommended sleep time
    """
    options = Options.Options
    options.sleep_time = 5 # test a high sleep time initially
    print('calibrating speed test...')
    calibration_results = process_query('yellow dog', options)

def speedtest_passed(results):
    """Returns whether a speedtest passed based on expected results

    Args:
        results (list[Product]): retrieved product results
    
    Returns:
        bool: True if given results match expected results, False otherwise
    """
    expected_length = 2
    expected_results = ['GOSIG GOLDEN', '701.327.90', 19.99, 4.9, 3, 2, 'GOSIG GOLDEN', '801.327.99', 9.99, 5, 3, 2]
    if len(results) != expected_length: return False
    i = 0
    for j in range(results):

