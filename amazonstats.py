from selectorlib import Extractor
from time import sleep
import re
import requests
import fileinput

# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('selectors.yml')


def scrape(url):

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
    r = requests.get(url, headers=headers)

    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n" % asin)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d" % (asin, r.status_code))
        return None

    # Pass the HTML of the page and create
    return e.extract(r.text)


for asin in fileinput.input():
    data = scrape("https://www.amazon.com/dp/product/" + asin.rstrip())

    title = data['title']

    author = data['author']
    if author is not None:
        author = re.sub(r'^.*\[', '', author)
        author = re.sub(r'\].*$', '', author)
    else:
        author = ""

    if data['sales_rank'] is None:
        sales_rank = ""
    else:
        sales_rank = data['sales_rank'].split()[4].replace("#", "").replace(",", "")

    if data['rating'] is None:
        rating = ""
    else:
        rating = data['rating'].split()[0]

    if data['number_of_ratings'] is None:
        number_of_ratings = ""
    else:
        number_of_ratings = data['number_of_ratings'].split()[0].replace(",", "")

    print(asin.rstrip(), title, author, sales_rank, rating, number_of_ratings, sep="\t", flush=True)

    sleep(2)
