import scrapy
from scrapy_splash import SplashRequest

script = """
    function main(splash, args)
      splash.private_mode_enabled = false
      headers = {
      ["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 
      Safari/537.36"
      }
      splash:set_custom_headers(headers)

      url = args.url
      assert(splash:go(url))
      assert(splash:wait(1))

      usd_tab = assert(splash:select(".filterPanel___2zFYQ > div:nth-of-type(3)"))
      usd_tab:mouse_click()

      splash:set_viewport_full()
      return splash:html()
    end
"""


class LivecoinSplashSpider(scrapy.Spider):
    name = 'livecoin_splash'
    allowed_domains = ['www.livecoin.net/en']
    start_urls = ["https://livecoin.net/en"]

    def start_requests(self):
        yield SplashRequest(url="https://www.livecoin.net/en", callback=parse_result, endpoint="execute", args={
            "lua_source": script
        })

    def parse_result(self, response):
        print(response.body)
