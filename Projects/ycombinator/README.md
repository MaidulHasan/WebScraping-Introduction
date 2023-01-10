**Starting the project** \
\$ scrapy startproject ycombinator \
\$ cd ycombinator \
\$ scrapy genspider ycombinator_jobs news.ycombinator.com

**Modifying the settings.py file** \
<u>Set:-</u> \
ROBOTSTXT_OBEY = False \
FEED_EXPORT_ENCODING = 'utf-8'

**Modifying the middlewares.py file to choose random user agent from a list of user agents to avoid getting banned**

    import logging
    import random

    from scrapy import signals
    from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


    class UserAgentRotatorMiddleware(UserAgentMiddleware):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 "
            "Safari/537.36 Edge/12.246",
            "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 "
            "Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 "
            "Safari/601.3.9",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
        ]

        def __init__(self, user_agent=""):
            self.user_agent = user_agent

        def process_request(self, request, spider):
            try:
                self.user_agent = random.choice(self.user_agents)
                request.headers.setdefault("User-Agent", self.user_agent)
            except IndexError:
                logging.error("Couldn't fetch the User Agent")
    }


**01. Working with the spider (ycombinator/ycombinator/spiders/ycombinator_jobs.py)**

Using proper css/xpath selectors extract the data that you want into local variables. You can check if your css/xpath selector is pulling the element you want or not by going to the scrapy shell and executing the code there. To launch a scrapy shell - \

\$ scrapy shell website_url

**02. Creating fields in (ycombinator/ycombinator/items.py) to store the scraped data**

**03. Yielding the scraped data to the created fields (in the ycombinator/ycombinator/spiders/ycombinator_jobs.py file)**

**04. Running the crawler** 

\$ scrapy crawl ycombinator_jobs -o jobs.json \

Here, the "-o jobs.json" command saves the output to the "jobs.json" file. We can change the file format to csv, xml etc. by simply changing the file extension. 

**05. Handling pagination**

Now that we have scraped our desired items from the first page, now we want to scrape similar items from the subsequent pages too. To deal with it we search for the "next page" button or similar elements that handles the pagination on the site. Also see if the link to the next page is absolute or relative url. It is also necessary to know when or where to stop. Define some condition when the scraper will stop. 

