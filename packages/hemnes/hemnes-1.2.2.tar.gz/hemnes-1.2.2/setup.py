import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hemnes",
    version="1.2.2",
    author="Sayeef Moyen",
    author_email="develop.sayeefrm@gmail.com",
    description="Ikea product scraper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sayeefrmoyen/hemnes",
    packages=setuptools.find_packages(exclude=("test",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='scraping ikea ikea-scraping python3 beautifulsoup, beautiful-soup',
    install_requires=['selenium', 'bs4', 'pytest'],
    python_requires='>=3',
)
