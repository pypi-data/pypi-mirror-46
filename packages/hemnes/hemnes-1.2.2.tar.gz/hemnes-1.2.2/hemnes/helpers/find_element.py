""""Functionality for locating items of interest on Ikea pages & anything related to directly interacting with html.

Attributes:
  * COLORS: set of colors to look for on product pages

Exceptions:

Todo:

"""

COLORS = {
    'alizarin',
    'amaranth',
    'amber',
    'amethyst',
    'apricot',
    'aqua',
    'aquamarine',
    'asparagus',
    'auburn',
    'azure',
    'beige',
    'bistre',
    'black',
    'blue',
    'brass',
    'bronze',
    'brown',
    'buff',
    'burgundy',
    'burnt',
    'camouflage',
    'caput',
    'cardinal',
    'carmine',
    'carrot',
    'celadon',
    'cerise',
    'cerulean',
    'champagne',
    'charcoal',
    'chartreuse',
    'cherry',
    'chestnut',
    'chocolate',
    'cinnabar',
    'cinnamon',
    'cobalt',
    'copper',
    'coral',
    'corn',
    'cornflower',
    'cream',
    'crimson',
    'cyan',
    'dandelion',
    'denim',
    'ecru',
    'emerald',
    'eggplant',
    'fern',
    'firebrick',
    'flax',
    'forest',
    'fuchsia',
    'gamboge',
    'gold',
    'golden',
    'goldenrod',
    'green',
    'gray',
    'grey',
    'harlequin',
    'heliotrope',
    'indigo',
    'ivory',
    'jade',
    'khaki',
    'lavender',
    'lemon',
    'lilac',
    'lime',
    'linen',
    'maegnta',
    'magnolia',
    'malachite',
    'maroon',
    'mauve',
    'midnight',
    'mint',
    'mist',
    'moss',
    'mustard',
    'myrtle',
    'navy',
    'ochre',
    'olive',
    'olivine',
    'orange',
    'orchid',
    'papaya',
    'peach',
    'pear',
    'periwinkle',
    'persimmon',
    'pine',
    'pink',
    'platinum',
    'plum',
    'powder',
    'puce',
    'prussian',
    'pumpkin',
    'purple',
    'quartz',
    'razzmatazz',
    'red',
    'robin',
    'rose',
    'royal',
    'ruby',
    'russet',
    'rust',
    'saffron',
    'salmon',
    'sand',
    'sandy',
    'sangria',
    'sapphire',
    'scarlet',
    'sea',
    'seashell',
    'sepia',
    'shamrock',
    'silver',
    'sky',
    'slate',
    'smalt',
    'steel',
    'tan',
    'tangerine',
    'taupe',
    'teal',
    'tenne',
    'tawny',
    'thistle',
    'titanium',
    'tomato',
    'turquoise',
    'ultramarine',
    'vermilion',
    'violet',
    'viridian',
    'wheat',
    'white',
    'wisteria',
    'xanthic',
    'yellow',
    'zucchini'
}

import re

def search_results_find_product_urls(soup):
    """Returns the urls to all of the products on a page of search results.

    Args:
        soup (BeautifulSoup): soup of a page of search results

    Returns:
        list[str]: product urls found on the page
    """
    return [product_wrapper.find('a')['href'].strip() for product_wrapper in soup.find_all('div', class_='product-compact__spacer')]

def product_page_find_product_name(soup):
    """Returns the name of the product on a product page.

    Args:
        soup (BeautifulSoup): soup of a product page

    Returns:
        str: name of the product
    """
    
    name_container = soup.find('span', id='name')
    try:
        return re.sub(r'[\s/-]+', ' ', name_container.string.strip())
    except Exception:
        return None

def product_page_find_product_id(soup):
    """Returns the id of the product on a product page.

    Args:
        soup (BeautifulSoup): soup of a product page

    Returns:
        str: id of the product
    """
    id_container = soup.find('div', id='itemNumber')
    try:
        return id_container.string.strip()
    except Exception:
        return None

def product_page_find_product_price(soup):
    """Returns the price of the product on a product page

    Args:
        soup (BeautifulSoup): soup of a product page

    Returns:
        float: price of the product
    """
    price_container = soup.find('span', id='price1')
    try:
        return float(price_container.string.strip().replace('$', '').replace('/', '').replace('\\', '').replace('-', '').replace(',', ''))
    except Exception:
        return None
    
def product_page_find_product_rating(soup):
    """Returns the custom rating of the product on a product page.

    Args:
        soup (BeautifulSoup): soup of a product page

    Returns:
        float: rating of the product
    """
    rating_container = soup.find('div', id='ratingStarsReview')
    try:
        return float(rating_container.find('a').string.strip())
    except Exception:
        return None

def product_page_find_product_images(soup):
    """Returns a list of product img urls on a product page.

    Args:
        soup (BeautifulSoup): soup of a product page

    Returns:
        list[str]: urls to images of the product
    """
    image_urls = []
    num_of_thumb_images = len(soup.find_all('div', class_='imageThumb'))
    if num_of_thumb_images > 0:
        # go through each thumbnail to get their urls
        for i in range(num_of_thumb_images):
            try:
                css_id = 'imgID_%d' % (i)            
                full_url = 'https://www.ikea.com%s' % (soup.find('img', id=css_id)['src'].strip())
                image_urls.append(full_url)
            except Exception:
                continue # skip over problematic urls
    else:
        # if there are no thumb images, find the main product image
        try:
            full_url = 'https://www.ikea.com%s' % (soup.find('img', id='productImg')['src'].strip())
            image_urls.append(full_url)
        except Exception:
            return None # if there are no images, return None
    return image_urls

def product_page_find_product_colors(soup):
    """Returns a list of colors associated with a product on a product page.

    Args:
        soup (BeautifulSoup): soup of a product page

    Returns:
        list[str]: colors of the product
    """
    short_descr_container = soup.find('span', class_='productType')
    try:
        short_descr_words = [word.lower() for word in short_descr_container.string.strip().replace(',', ' ').replace('/', ' ').replace('-', ' ').split()]
        # this is a set to avoid keeping duplicates
        colors = {color for color in short_descr_words if color in COLORS}
        return list(colors) if len(colors) > 0 else None
    except Exception:
        return None

def product_page_has_keywords(soup, keywords, strict=False):
    """Returns whether a product's description has all or some keywords

    Args:
        soup (BeautifulSoup): soup of a product page
        keywords (set[str]): required keywords
        strict (bool): True if all of the keywords are required, False otherwise

    Returns:
        bool: True if keywords with specified strictness are found
    """
    short_descr_container = soup.find('span', class_='productType')
    # first check the short description
    if short_descr_container is not None:
        short_descr_words = get_words_from_text(short_descr_container.string)
        for word in short_descr_words:
            if word in keywords:
                if not strict: return True
                keywords.remove(word)
                if len(keywords) == 0: return True # don't continue if all words found

    long_descr_container = soup.find('div', id='salesArg')
    # check the longer description
    if long_descr_container is not None:
        long_descr_words = get_words_from_text(long_descr_container.string)
        for word in long_descr_words:
            if word in keywords:
                if not strict: return True
                keywords.remove(word)
                if len(keywords) == 0: return True 

    detailed_descr_container = soup.find('div', id='custBenefit')
    # the detailed description is a <ul>
    key_points = detailed_descr_container.find_all('li') if detailed_descr_container is not None else []
    # last, check the detailed product information
    for point in key_points:
        point_words = get_words_from_text(point.string) if point.string is not None else get_words_from_text(point.find('t').string) # the first element always has a <t> child
        for word in point_words:
            if word in keywords:
                if not strict: return True
                keywords.remove(word)
                if len(keywords) == 0: return True

    return False

def get_words_from_text(text):
    """Returns a list of words (lowercase) found in some text.

    Args:
        text (str): some string

    Returns:
        list[str]: words found
    """
    return [word.lower() for word in text.strip().replace(',', ' ').replace('/', ' ').replace('-', ' ').replace('.', ' ').split()]
