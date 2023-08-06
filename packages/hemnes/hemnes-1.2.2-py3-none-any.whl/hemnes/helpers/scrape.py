"""Functionality for scraping or related to hemnes 'life-cycle'.

Attributes:

Exceptions:

Todo:

"""

from hemnes.helpers import Logger, PageFetcher, Product, find_element, url_generator

def get_product_from_page(soup, url, tag=None, logger=None):
    """Returns a Product representation of a product page.

    Args:
        soup (BeautifulSoup): soup of the product page
        url (str): url to a product page
        tag (str): meta tag
        logger (Logger): Logger object

    Returns:
        Product: Product object
    """
    try:
        prod_name = find_element.product_page_find_product_name(soup)
        prod_id = find_element.product_page_find_product_id(soup)
        prod_price = find_element.product_page_find_product_price(soup)
        prod_url = url
        prod_rating = find_element.product_page_find_product_rating(soup)
        prod_img_urls = find_element.product_page_find_product_images(soup)
        prod_colors = find_element.product_page_find_product_colors(soup)
        prod_tag = tag
        return Product.Product(prod_name, prod_id, prod_price, prod_url, prod_rating, prod_img_urls, prod_colors, prod_tag)
    except Exception:
        if logger is not None:
            logger.log('ERROR: failed to process product %s - skipping' % (url))
        return None

def get_products_from_urls(pf, prod_urls, num_desired = None, keywords=None, strict=False, tag=None, logger=None):
    """Returns a list of Products from a list of product urls.

    Args:
        pf (PageFetcher): PageFetcher object
        prod_urls (list[str]): urls to product pages
        num_desired (int): number of desired products - assumed to be all products if unspecified
        keywords (set[str]): required keywords for returned products
        strict (bool): True if all keywords are required, False otherwise
        tag (str): meta tag to include in Products
        logger (Logger): Logger object

    Returns:
        list[Product]: valid Products found
    """
    products = []
    try:
        for url in prod_urls:
            try:
                soup = pf.get_soup(url)
            except Exception:
                if logger is not None: logger.log('ERROR: problem loading page %s - skipping' % (url))
                continue
            if keywords is not None and not find_element.product_page_has_keywords(soup, keywords, strict):
                if logger is not None: logger.log('WARN: product %s missing required keywords - skipping' % (url))
                continue
            product = get_product_from_page(soup, url, tag, logger)
            if product is not None: products.append(product)
            if logger is not None: logger.log('OK: found valid product %s' % (url))
            if num_desired is not None and len(products) == num_desired: return products # pre-emptive return if we found the target number of products
    except Exception:
        if logger is not None: logger.log('ERROR: unexpected failure in processing %d products - salvaging %d found products' % (len(prod_urls), len(products)))
    finally:
        return products

def process_query(pf, query, num_desired=None, keywords=None, strict=False, tag=None, logger=None):
    """Returns a list of Products found for a query.

    Args:
        pf (PageFetcher): PageFetcher object
        query (str): query word(s)
        num_desired (int): number of desired products - assumed to be as many as possible in unspecified
        keywords (set[str]): required keywords
        strict (bool): True if all keywords required, False otherwise
        tag (str): meta parameter
        logger (Logger): Logger object

    Returns:
        list[Product]: Products found for the query
    """
    if logger is not None: logger.log('OK: running hemnes process_query on query: %s' % (query))
    products = []
    try:
        page_num = 1
        prod_urls = None
        while (num_desired is None or len(products) != num_desired) and (prod_urls is None or len(prod_urls) != 0):
            prod_urls = find_element.search_results_find_product_urls(pf.get_soup(url_generator.get_url_for_search_results(query, page_num)))
            remaining_num_desired = None if num_desired is None else num_desired-len(products)
            next_products = get_products_from_urls(pf, prod_urls, remaining_num_desired, keywords, strict, tag, logger)
            products.extend(next_products)
            page_num += 1
    except Exception:
        if logger is not None: logger.log('ERROR: unexpected failure in process_query - salvaging %d found products' % (len(products)))
    finally:
        if logger is not None:
             if num_desired is not None and len(products) != num_desired: logger.log('WARN: only found %d of %d requested products' % (len(products), num_desired))
             elif num_desired is None: logger.log('OK: returning %d products' % (len(products)))
        return products # return any results found
