from random import randint
from selectorlib import Extractor
from time import sleep
import re
import requests
import fileinput

# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('selectors.yml')


def scrape(base_url, asin):

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    r = requests.get(base_url + asin, headers=headers)

    # Simple check to check if page was blocked
    if 'To discuss automated access to Amazon data please contact' in r.text:
        print('Page %s was blocked by Amazon. Please try using better proxies\n' % asin)
        return None

    if r.status_code > 500:
        print('Page %s must have been blocked by Amazon as the status code was %d' % (asin, r.status_code))
        return None

    # Parse the HTML of the page and create a dictionary with the requested data
    return e.extract(r.text)


for asin in fileinput.input():
    asin = asin.rstrip()
    data = scrape('https://www.amazon.com/dp/product/', asin)

    if data is None:
        print(asin, 'None', sep='\t', flush=True)
        sleep(randint(2, 5))
        continue

    title = ''
    author = ''
    rating = ''
    number_of_ratings = ''
    sales_rank = ''

    if data['title'] is not None:
        title = data['title']

    if data['author'] is not None:
        author = data['author']
        author = re.sub(r'^.*\[', '', author)
        author = re.sub(r'\].*$', '', author)

    if data['rating'] is not None:
        rating = data['rating'].split()[0]

    if data['number_of_ratings'] is not None:
        number_of_ratings = data['number_of_ratings'].split()[0].replace(',', '')

    if data['details'] is not None:
        split_details = data['details'].split()
        for i in range(len(split_details)):
            if split_details[i] == 'Rank:':
                sales_rank = split_details[i+1].replace('#', '').replace(',', '')

    print(asin, title, author, sales_rank, rating, number_of_ratings, sep='\t', flush=True)

    sleep(randint(2, 5))
