from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

class PageFetcher:
    """Class offering functionality for fetching pages over the web and retrieving BeautifulSoup page-representations.

    This functionality is separated out into its own class in the hope that one
    day there will be a better way of scraping javascript-generated webpages, and 
    when that day comes, this package will have been setup properly to adapt to that quickly.
    """

    def __init__(self, chromedriver_path=None, sleep_time=3):
        """Default PageFetcher constructor.

        Args:
            chromedriver_path (str): path to ChromeDriver binary
            sleep_time (int): time to wait for pages to load before retrieving DOM
        """
        # selenium webdriver setup
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(chromedriver_path, options=options) if chromedriver_path is not None else webdriver.Chrome(options=options)
        
        self.__driver = driver
        self.__sleep_time = sleep_time        

    def get_soup(self, url):
        """Returns the BeautifulSoup of a webpage.

        Args:
            url (str): desired webpage

        Returns:
            BeautifulSoup: soup of the webpage
        """
        self.__driver.get(url)
        sleep(self.__sleep_time)
        return BeautifulSoup(self.__driver.page_source, 'html.parser')

    def close(self):
        """Closes any open connections or resources."""
        self.__driver.close()
        self.__driver.quit()
