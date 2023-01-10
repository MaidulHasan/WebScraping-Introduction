import scrapy
from scrapy.selector import Selector  # to convert string object to selector object so that we can scrape it.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from shutil import which
from ..items import LivecoinItem


class LivecoinSeleniumSpider(scrapy.Spider):
    name = 'livecoin_selenium'
    allowed_domains = ['www.livecoin.net/en']
    start_urls = ["https://livecoin.net/en"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        driver_path = which("chromedriver")

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
        driver.set_window_size(1920, 1080)
        driver.get("https://livecoin.net/en")

        usd_tab = driver.find_element_by_css_selector(".filterPanel___2zFYQ > div:nth-of-type(3)")
        usd_tab.click()

        self.html = driver.page_source
        # driver.implicitly_wait(5)
        driver.close()
        # print(self.html)

    def parse(self, response):
        response = Selector(text=self.html)
        for row in response.css(".ReactVirtualized__Table__row"):
            yield {
                "currency": row.css("div[aria-colindex='1'] div::text").extract()[0],
                "volume": row.css("div[aria-colindex='2'] span::text").extract()[0],
                "last_price": row.css("div[aria-colindex='3'] span::text").extract()[0]
            }
