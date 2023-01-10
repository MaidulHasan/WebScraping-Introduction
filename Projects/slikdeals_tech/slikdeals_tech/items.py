# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SlikdealsTechItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    old_price = scrapy.Field()
    product_rating = scrapy.Field()
    no_of_ratings = scrapy.Field()
    product_link = scrapy.Field()
    user_agent = scrapy.Field()
