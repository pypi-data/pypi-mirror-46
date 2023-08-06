""""Functionality for generating urls for Ikea queries.

Attributes:

Exceptions:

Todo:

"""

import re

__PRODUCTS_PER_PAGE = 40

def get_url_for_search_results(query, page_number):
    """Returns the url for a page of search results for a query.

    Args:
        query (str): query words
        page_number (int): desired page

    Returns:
        str: url for a page of search results
    """
    urlified_query = re.sub(r'\s+', '+', query.strip())
    start_row = (page_number-1)*__PRODUCTS_PER_PAGE
    return 'https://www.ikea.com/ms/en_US/usearch/?&query=%s&rows=40&view=grid&start=%d' % (urlified_query, start_row)
