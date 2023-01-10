import scrapy
from ..items import FotmobItem
import re


class LeagueFixtureSpider(scrapy.Spider):
    name = 'laliga_fixture'
    allowed_domains = ['www.fotmob.com']
    start_urls = ['https://www.fotmob.com/leagues/87/matches/laliga/']

    def parse(self, response):
        matches = response.css("a.css-1cqumcw-MatchCSS::attr(href)").extract()
        for match in matches:
            yield response.follow(url=match, callback=self.parse_match_details,
                                  meta=dict(relative_link=match))

    def parse_match_details(self, response):
        item = FotmobItem()
        date_time = response.css(
            ".css-quhg9a-mfContentBlock-applyHover-infoBoxWrapper > span:nth-of-type(2)::text").extract()
        home_team = response.css("a:nth-of-type(1) > .css-1nd2gq0-mfHeaderTeamTitle.eb9uzl81::text").extract()
        opponent_team = response.css("a:nth-of-type(2) > .css-1nd2gq0-mfHeaderTeamTitle.eb9uzl81::text").extract()
        match_status = response.css("span.css-1iup54y-bottomRow::text").extract()
        if re.match(r"[a-zA-Z]+ [0-9]+, [0-9]+", match_status[0]):
            match_status = "Not Played Yet"
            match_result = "Unavailable"
        else:
            match_result = response.css("span.css-4rm8lc-topRow::text").extract()

        fotmob_link = "www.fotmob.com" + response.request.meta["relative_link"]

        item["date_time"] = date_time
        item["home_team"] = home_team[0]
        item["opponent_team"] = opponent_team[0]
        item["match_status"] = match_status
        item["match_result"] = match_result
        item["fotmob_link"] = fotmob_link

        yield item
