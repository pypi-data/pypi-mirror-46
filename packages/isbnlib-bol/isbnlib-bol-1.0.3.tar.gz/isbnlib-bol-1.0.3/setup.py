from setuptools import setup

setup(name="isbnlib-bol",
      version="1.0.3",
      description="ISBN lookup for Bol.com",
      packages=['isbnlib_bol'],
      author="Stan Janssen",
      author_email="pypi@finetuned.nl",
      url="https://git.finetuned.nl/stan/isbnlib-bol",
      entry_points = {
        'isbnlib.metadata': ['bol=isbnlib_bol:query']
      },
      install_requires=['requests', 'bs4', 'isbnlib'])