#!/usr/bin/env python

"""Queries Amazon for details about a list of products (asins)"""

import sys
import fileinput

from amazonconfig import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AMAZON_ASSOCIATE_TAG
from amazon.api import AmazonAPI, AsinNotFound
from BeautifulSoup import BeautifulSoup
from time import sleep
from urllib2 import urlopen, HTTPError

def lookup(asin):
    """Looks up the asin in Amazon and print details about it"""
    try:
        product = amazon.lookup(IdType='ISBN', SearchIndex='Books', ItemId=asin)
    except AsinNotFound:
        return str(asin) + '\tNot Found'

    if isinstance(product, list):
        product = product[0]

    price = product.list_price[0]
    sales_rank = product._safe_get_element('SalesRank')

    reviews_url = product.reviews[1]

    reviews = None

    while not reviews:
        try:
            reviews = urlopen(reviews_url)
        except HTTPError:
            # let us wait one second and we try again
            sleep(1)

    soup = BeautifulSoup(reviews)
    span = soup.find('span', {'class': 'crAvgStars'})

    if span is None:
        return str(asin) + '\t' + 'No reviews'

    avg_rating = span.contents[0].contents[1].contents[0]['alt'].split()[0]
    num_ratings = span.contents[2].contents[0].split()[0]

    return str(asin) + '\t' + str(sales_rank) + '\t' + str(price) + '\t' + str(avg_rating) + '\t' + str(num_ratings)

# The main program which connects to Amazon
# and queries the API for details about a
# list of asins
amazon = AmazonAPI(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AMAZON_ASSOCIATE_TAG, MaxQPS=0.9)

for line in fileinput.input():
    an_asin = line.rstrip('\n')
    sys.stdout.write(lookup(an_asin) + '\n')
    sys.stdout.flush()
