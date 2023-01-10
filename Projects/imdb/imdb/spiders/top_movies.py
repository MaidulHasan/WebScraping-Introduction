import scrapy
from scrapy_selenium import SeleniumRequest
from ..items import ImdbItem


class TopMoviesSpider(scrapy.Spider):
    name = 'top_movies'

    def start_requests(self):
        yield SeleniumRequest(url="https://www.imdb.com/chart/top/?ref_=nv_mv_250", callback=self.get_movie_links)

    def get_movie_links(self, response):
        movie_links = response.css("td.titleColumn a::attr(href)").extract()
        for movie_link in movie_links:
            yield SeleniumRequest(url="https://www.imdb.com" + movie_link, callback=self.parse_movie_details)

    def parse_movie_details(self, response):
        item = ImdbItem()
        item["title"] = response.xpath(
            "normalize-space(/html//div[@id='title-overview-widget']/div[@class='vital']//h1/text())").extract_first()
        item["rating"] = response.css("[itemprop='ratingValue']::text").extract_first()
        item["runtime"] = response.xpath(
            "normalize-space(/html//div[@id='title-overview-widget']/div[@class='vital']/div["
            "@class='title_block']//time[1]/text())").extract_first()
        item["release_year"] = response.css("#titleYear a::text").extract_first()
        item["genre"] = response.css(".subtext > a:nth-of-type(1)::text").extract_first()

        yield item
