import scrapy
from scrapy_selenium import SeleniumRequest
import re
from ..items import SlikdealsTechItem


class TechSpider(scrapy.Spider):
    name = 'tech'

    def start_requests(self):
        yield SeleniumRequest(
            url="https://slickdeals.net/deals/tech/",
            callback=self.parse
        )

    def parse(self, response):
        next_page = response.css("a.button[data-role]::attr(href)").extract_first()
        deal_links = response.css("a.itemTitle.bp-c-link::attr(href)").extract()
        for link in deal_links:
            yield SeleniumRequest(
                url="https://www.slickdeals.net" + link,
                callback=self.parse_item
            )

        if next_page:
            yield SeleniumRequest(
                url="https://www.slickdeals.net" + next_page,
                callback=self.parse
            )

    # def normalize_space(self, string):
    #     string = string.strip()
    #     string = re.sub(r'\s+', ' ', string)
    #     return string

    def parse_item(self, response):
        item = SlikdealsTechItem()

        item["product_name"] = (response.xpath("normalize-space(//div[@id='dealTitle']/h1[1]/text())").extract()[0])

        item["product_price"] = response.css("div.dealPrice.floatLeft::text").extract()[0]

        old_price = response.css(".detailLeftColumn .oldListPrice::text").extract()
        try:
            item["old_price"] = old_price[0]
        except IndexError:
            item["old_price"] = "Not Available"

        product_rating = response.css("#productRating::attr(data-rating)").extract()
        try:
            item["product_rating"] = product_rating[0]
        except IndexError:
            item["product_rating"] = "Not Available"

        no_of_ratings = response.css("#productRating::attr(data-total-reviews)").extract()
        try:
            item["no_of_ratings"] = no_of_ratings[0]
        except IndexError:
            item["no_of_ratings"] = "Not Available"

        item["product_link"] = response.css("a#largeBuyNow::attr(href)").extract()[0]

        item["user_agent"] = response.request.headers.get("User-Agent").decode("utf-8")

        yield item
