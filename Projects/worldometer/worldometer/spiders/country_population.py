import scrapy

from ..items import WorldometerItem


class CountryPopulationSpider(scrapy.Spider):
    name = 'country_population'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['http://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        relative_links = response.css("td a::attr(href)").extract()
        for relative_link in relative_links:
            yield response.follow(url=relative_link, callback=self.parse_country)

    def parse_country(self, response):
        item = WorldometerItem()
        country = response.css("li.active::text").extract()
        years = response.css("div.table-responsive table tr td:nth-child(1)::text").extract()
        population = response.css("div.table-responsive table tr td :nth-child(1)::text").extract()
        # div.table-responsive table tr td:nth-child(1) strong

        item["country"] = country
        item["years"] = years[0:18]  # we need the first table and first 18 of all the selected rows are of table-1
        item["population"] = population[0:18]

        yield item
