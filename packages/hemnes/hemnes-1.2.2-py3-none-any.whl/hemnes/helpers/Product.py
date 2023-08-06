class Product:
    """Class to encapsulate stored product data.

    Attributes:
        name (str): name of the product
        id_no (str): product id
        price (float): price of the product
        url (str): url to the product page
        rating (float): customer rating of the product (None-able)
        img_urls (list[str]): urls to product images (None-able)
        colors (list[str]): colors associated with the product (None-able)
        tag (str): meta tag
    """

    def __init__(self, name, id_no, price, url, rating, img_urls, colors, tag=None):
        """Default Product constructor.

        The rating, img_urls, and colors fields are all None-able

        Args:
            name (str): name of the product
            id_no (str): product id
            price (float): price of the product
            url (str): url to the product page
            rating (float): user rating of the product
            img_urls (list[str]): urls to product images
            colors (list[str]): colors associated with the product
            tag (str): meta tag
        """
        self.name = name
        self.id_no = id_no
        self.price = price
        self.url = url
        self.rating = rating
        self.img_urls = img_urls
        self.colors = colors
        self.tag = tag

    def to_dict(self):
        """Returns a dict representation of a Product."""
        return {
            'name': self.name,
            'id_no': self.id_no,
            'price': self.price,
            'url': self.url,
            'rating': self.rating,
            'img_urls': self.img_urls,
            'colors': self.colors,
            'tag': self.tag
        }
