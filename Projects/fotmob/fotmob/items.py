# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FotmobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date_time = scrapy.Field()
    home_team = scrapy.Field()
    opponent_team = scrapy.Field()
    match_status = scrapy.Field()
    match_result = scrapy.Field()
    fotmob_link = scrapy.Field()
