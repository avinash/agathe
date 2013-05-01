# Agathe

Given a list of Amazon ASINs, retrieve detailed information from Amazon. Useful for deciding what Kindle book to read for example.

## Requirements

Please install the following using easy_install or pip:

	BeautifulSoup
	python-amazon-simple-product-api

## Quick Start

Copy amazononfig.py.sample to amazonconfig.py and update AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY and AMAZON_ASSOCIATE_TAG. Then, use either a pipe to send ASINs to the script (one per line)
    
	echo "12345678" | python amazonstats.py
	cat amazonASINs | python amazonstats.py

or use a filename as a parameter to the amazonstats.py script

	python amazonstats.py amazonASINs

The result is typically:

	B002WE46UW	2604	22.0	4.6	1,548
	B000WJVK26	335	11.95	4.3	1,590
	B004J4XGN6	1414	26.0	4.4	316
	B0026772N8	2369	12.99	4.0	755
	B000RO9VJK	3809	15.99	4.4	651

The five columns represent (1) the Amazon ASIN, (2) the sales rank, (3) the price, (4) the average rating obtained and (5) the number of ratings on the Amazon website.

## Possible use

I personally use this script to create a CSV (but tab separated...) which I open in a spreadsheet. This then allows me to sort the ASINs using the various columns to help me decide what to read on my Kindle. Your milleage may vary.

## Project Authors

[Avinash Meetoo](http://www.avinashmeetoo.com/)
