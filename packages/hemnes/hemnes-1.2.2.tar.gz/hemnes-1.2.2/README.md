
<!-- HEADER INFORMATION -->
<h3 align="center"><a href="https://pypi.org/project/hemnes/">HEMNES</a></h3>

<p align="center">
    <a href="https://github.com/sayeefrmoyen/hemnes/issues">Report Bug</a>
    ·
    <a href="https://github.com/sayeefrmoyen/hemnes/issues">Request Feature</a>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
  * [Why Selenium or Why not Python Requests](#why-selenium-or-why-not-python-requests)
* [Getting Started](#getting-started)
  * [Runtime](#runtime)
  * [Installation](#install)
  * [Basic Usage](#basic-usage)
* [Product Object Details](#product-object-details)
* [Advanced Usage](#advanced-usage)
   * [Specifying the path to ChromeDriver](#specifying-the-path-to-the-chromedriver-binary)
   * [Required Keywords & Strict Search](#required-keywords-&-strict-searching)
   * [Logging](#enable-logging)
   * [Retrieving a Specific Number of Results](#retrieving-a-specific-number-of-results)
   * [Speeding Up](#speeding-up)
   * [Using the Tag Field](#using-product's-tag-field)
   * [Writing Results to JSON/CSV](#writing-results-to-json-or-csv)
* [Tests](#tests)
* [What's Next](#what's-next)
* [Release History](#release-history)
* [License](#license)

# About the Project

**Hemnes is a pip package for scraping product data from ikea**, built because **rewriting scrapers is a waste of time**. Hemnes gets you to the point of being able to query Ikea's product catalog in less than 30 seconds (I didn't time this). 

**The following product data is collected by Hemnes**:

* `name (str)` - name of the product
* `id (str)` - unique product id
* `price (float)` - product price
* `url (str)` - url to product page
* `rating (float)` - average customer rating
* `img_urls (list[str])` - urls to product images
* `colors (list[str])` - product colors (see `COLORS` in `hemnes/helpers/find_element`for a full list of colors being searched for)

Hemnes comes equipped with a bit of helpful functionality for doing things like:

* finding products with specific keywords in their descriptions
* logging
* writing results to JSON

[Read more about extended functionality here](#additional-options)

### Built With

* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
* [ChromeDriver](http://chromedriver.chromium.org)
* [PyTest](https://docs.pytest.org/en/latest/)
* [Selenium WebDriver](https://www.seleniumhq.org/docs/03_webdriver.jsp)

### Why Selenium or Why not Python Requests

If you do a quick browse through stack overflow posts about scraping ikea - or if you are considering writing a scraper yourself - you will probably come across people using selenium Webdriver for pages that don't need it. Selenium is heavier than python requests, however, **webdriver can load angular generated content whereas requests cannot**.

Ikea's current website uses angular for its search results. This is a change from its older search, which was accessible via python requests. The new search provides more accurate results, and less garbage. Speaking from experience, the old search is really terrible and provides a number of trash results for any given query that I had trouble connecting back to my original search (one example of this is the old search returning 58 pages of results for 'table', which included things like placemats and dog toys; the new search returns 15, and all of the results are actually tables)

# Getting Started

Hemnes is pretty straightforward to install and use. It functions exactly as you would expect a web-scraping package to function - enter a query and get results back.

### Runtime

* Python 3+

### Installation

Hemnes is installed using standard pip installation. To install from PyPI run

```bash
pip3 install hemnes
```

Alternatively, you can clone the repo and then run pip install inside the directory

```bash
# clone the repository
git clone https://github.com/sayeefrmoyen/hemnes.git
cd hemnes
pip3 install . # install the current directory as a package
```

#### ChromeDriver

Hemnes uses [ChromeDriver](http://chromedriver.chromium.org) to load webpages.  If ChromeDriver is already installed and on your syspath you can skip the rest of this section.

To use ChromeDriver you will need to [install Google Chrome](https://www.google.com/chrome/). If you already have google chrome installed *I believe that you should be able to run Hemnes without a problem*. For full disclosure, I am not familiar with the google chrome or chrome driver code, and do not know how they interact, but I have had no issues running Hemnes without ever explicitly installing the ChromeDriver binary.

With that said, Selenium's documentation for WebDriver suggests that you install both a version of Google Chrome and ChromeDriver. If you find that after installing Google Chrome you are still receiving errors regarding ChromeDriver, then you should proceed to [install ChromeDriver](https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver).

At this point, you should be ready to start using Hemnes.

### Basic Usage

At its simplest, Hemnes only requires a query. Use the `process_query` function to retrieve product data for a given query. `process_query` returns a `list[Product]` containing the products matching the given query.

```python
import hemnes

# query ikea's product catalog for products tagged as chairs
# chair_results is now a list[Product] containing all of the products
# in ikea's catalog of chairs
results = hemnes.process_query('chair')
```

# Product Object Details

Hemnes returns query results in the form of a `list[Product]`. `Product` is a helper class containing the following fields:

* `name (str)` - name of the product
* `id (str)` - unique product id
* `price (float)` - product price
* `url (str)` - url to product page
* `rating (float)` - average customer rating
* `img_urls (list[str])` - urls to product images
* `colors (list[str])` - product colors
* `tag (str)` - flexible usage field

Most of these are rather self-explanatory; I'm only going to talk about the `tag` field in depth. The `tag` attribute is specified for all products returned by a single call to `process_query`, and is included for flexible use. One example of why such a field would be useful is if you were storing this data in a database and needed a primary key to search on - you could use `tag` to indicate the type of product (chair, table, etc.). By default `tag` is set to `None`. For more details on using tag, see [setting up additional options](#additional-options)

One more thing to note is that all of these fields, excluding `url`, have the potential to not be found, and subsequently being set to`None`. However, based on testing and examining the structure of Ikea's product webpages, it is unlikely that any of these attributes are unable to be found. The one exception to this rule is the `rating` field, which will be set to `None` any time the product has no reviews.

# Advanced Usage

Hemnes expects to be passed an`Options` object to specify a number of additional settings. `Options` is a helper class for organizing passing a large number of parameters to `process_query`. If you don't provide an `Options` object to `process_query`, a number of default settings are selected. The rest of this section will discuss how to modify those settings.

#### Specifying the path to the ChromeDriver binary

If you have installed the ChromeDriver binary and Google Chrome browser, but are still encountering errors when running Hemnes, you may need to explicitly pass the path to the binary to selenium Webdriver. To do so, use the `Options` class

```python
import hemnes
...
# explicitly passing the chromedriver binary to webdriver
options = hemnes.Options()
options.cdriver_path = 'path/to/chromedriver/binary'
results = hemnes.process_query('your query', options)
```

#### Required Keywords & Strict Searching

Sometimes it's necessary to refine your query beyond usual high-level query terms. Hemnes allows you to specify a number of `keywords` to search for on product pages, and only return products which contain all or some of those words. `Options` accepts setting the `keywords` field to a `set[str]` containing the desired keywords.

You can also specify whether or not all of the keywords should be required by setting `Options` `strict` field to a `bool`. By default, `strict` is set to `False`, meaning that if `keywords` are passed, any product with at least one keyword will be returned. To require that all `keywords` are found for returned products, set `strict` to `True`

```python
import hemnes
...
# setting required keywords
options = hemnes.Options()
options.keywords = {'large', 'comfortable'}
# enable strict-searching, requiring all products to contain all of the
# keywords in order to be returned. If disabled or untouched, any
# product with at least one of the keywords will be returned
options.strict = True
results = hemnes.process_query('chair', options)
```

For those who are curious about where `keywords` are being looked for, Hemnes searches through 3 different product description sections on each product's page for `keywords`.

#### Enable Logging

Some jobs for queries that return a large number of results may take a while to complete. Even for shorter jobs, it can be helpful to see where Hemnes is in processing a query. In order to enable logging process results, set the `log` field in `Options` to `True`. By default `log` is set to `False` to avoid overwhelming unsuspecting users.

```python
import hemnes
...
# enabling logs
options = hemnes.Options()
options.log = True
# enable logging - this will log to both stdout and to a
# logfile found at 'hemnes-logs/hemnes-MONTH-DAY-HOUR-MINUTE-SECOND.log
results = hemnes.process_query('chair', options)
```

By default logging will log to both stdout and to a log file that will look something like `hemnes-logs/hemnes-04-23-02:41:16.log` - the file is named `hemnes-MONTH-DAY-HOUR-MINUTE-SECOND.log`. If there is no `hemnes-logs` directory it will be created prior to trying to write files to it.

Hemnes will log things like:

* when a valid product is found
* when an invalid product is found (e.g. fails keyword requirements)
* total number of valid products to be returned
* any potential errors

#### Retrieving a Specific Number of Results

If you only need a specific number of results for a given query, set the `num_results` field of `Options`.

```python
import hemnes
...
# setting a target number of results
options = hemnes.Options()
options.num_results = 10
# hemnes will only return up to 10 products
results = hemnes.process_query('chair', options)
```

Hemnes will return the number of products requested, or fewer if the query did not return enough results.

#### Speeding Up

Loading angular pages can be slow, mostly because it takes time to retrieve full DOM from such pages. Altering the imposed sleep time for DOM to be fully loaded can drastically increase the speed of Hemnes.

By default, Hemnes requires a 3 second sleep time after each page request in order to insure that the DOM is fully loaded. For users with fast download speeds, this may be longer than is necessary. In order to reduce the sleep time after network requests, set the `sleep_time` attribute of `Options` to something more appropriate for your internet connection.

```python
import hemnes
...
# setting required keywords
options = hemnes.Options()
options.sleep_time = 1
# hemnes will now wait only 1 second for DOM to be loaded for
# newly retrieved pages. Users should set sleep_time to an
# appropriate amount of time based on their internet connection.
# The default setting of 3-seconds should be fine for almost all users
results = hemnes.process_query('chair', options)
```

#### Using Product's Tag Field

The `tag` field can be set for all returned `Product` for a given call to `process_query` by setting it in `Options`. `tag` should be of type `str`.

```python
import hemnes
...
# setting the tag attribute
options = hemnes.Options()
options.tag = 'chair'
# all of the products returned in results will have their tag field
# set to the string "chair"
results = hemnes.process_query('chair', options)
```

#### Writing Results to JSON or CSV

Storing scraped results to JSON or CSV can be done by setting the appropriate paths to the files using `Options`.
Hemnes will delete an existing file if the path already exists.

Note: any `None` fields will be written as `null` in JSON, or left empty in CSV

```python
import hemnes
...
options = hemnes.Options()
# setting the path to a JSON dump file
options.json_dump = 'path_to_json_file.json'
# setting the path to a CSV dump file
options.csv_dump = 'path_to_csv_file.csv'
# results will be written to the specified json or csv files
results = hemnes.process_query('chair', options)
```

# Tests

Tests are broken into `test_isolated` and `test_integrated`. `test_isolated` are, as they sound, true unit-tests for individual functionality. `test_integrated` are tests for higher-level functionality that depends on some of the lower level functionality provided by functions tested in `test_isolated`.

Note: `test_integrated` take a bit of time to execute as they go through the entire process of retrieving product data from start to finish

To run the tests clone the repository and run using **pytest**

```bash
# install pytest if you do not have pytest installed
pip3 install pytest
# clone the repository
git clone https://github.com/sayeefrmoyen/hemnes.git
cd hemnes
# --verbose flag is optional - provides helpful console output
pytest --verbose # run all of the tests
pytest test/test_isolated.py --verbose # only run isolation tests
pytest test/test_integrated.py --verbose # only run intregration tests
```

# What's Next

I'm ok with where this is now - if anyone requests more features I will look into them, but otherwise I will be maintaining hemnes as-is.

# Release History

* 1.2 - add saving to csv
* 1.1 - add saving to json
* 1.0 - first stable, tested release
* 0.*.\* - pre-test releases

# License

Distributed under the MIT License. See LICENSE for more information.
