#!/usr/bin/env python

"""Queries Amazon for details about a list of products (asins)"""

import sys
import fileinput

from amazonconfig import KEY, SECRET, TAG, COUNTRY
from amazon.paapi import AmazonAPI
from bs4 import BeautifulSoup
from time import sleep
from urllib.request import urlopen, HTTPError

def get_product(asin):
    """Looks up the asin in Amazon and print details about it"""
    product = amazon.get_product(asin)

    """soup = BeautifulSoup(reviews)
    span = soup.find('span', {'class': 'crAvgStars'})

    if span is None:
        return str(asin) + '\t' + 'No reviews'

    avg_rating = span.contents[0].contents[1].contents[0]['alt'].split()[0]
    num_ratings = span.contents[2].contents[0].split()[0]

    return str(asin) + '\t' + str(sales_rank) + '\t' + str(price) + '\t' + str(avg_rating) + '\t' + str(num_ratings)"""
    return product

# The main program which connects to Amazon
# and queries the API for details about a
# list of asins
amazon = AmazonAPI(KEY, SECRET, TAG, COUNTRY)

for line in fileinput.input():
    an_asin = line.rstrip('\n')
    sys.stdout.write(get_product(an_asin) + '\n')
    sys.stdout.flush()
