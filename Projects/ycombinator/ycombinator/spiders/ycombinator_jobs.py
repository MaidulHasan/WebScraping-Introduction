import scrapy

# We clean and store the scraped data in the fields that we created in the items.py file. 
# To access the fields we import the YcombinatorItem class from the items.py file.
from ..items import YcombinatorItem

# To obtain an absolute url we import urllib.parse and use the urljoin() method. 
import urllib.parse

class YcombinatorJobsSpider(scrapy.Spider):
    name = 'ycombinator_jobs'
    allowed_domains = ['news.ycombinator.com']
    # start_urls defines the urls from where to get the http response from 
    start_urls = ['https://news.ycombinator.com/jobs']

    # instead of start urls we can use scrapy.Request method to handle the initial request.
    
    # def start_requests(self):
    #     yield scrapy.Request(url='https://news.ycombinator.com/jobs', callback=self.parse)

    page = 0 # to keep track of how many pages we have scraped

    # the parse method grabs the http code of the url defined in the start_urls list and returns them as the response. then we can manipulate this response object to extract our desired information using the proper css or xpath selector.
    def parse(self, response):
        # first we work with the "Jobs" page. We want to extract the title of each job posting, the link to that listing, the time when the job was listed. We also want to be able to filter out posts that has certain keywords in them so that we only see the posts that we are interested in.
        
        # Extracting Titles (returns a list)
        titles = response.css("tr.athing .titlelink::text").extract()
        # .extract() returns a list of all the different texts/titles selected by the defined css tag.
        # Some methods that works similarly to extract() are get() and extract_first(). These methods gets you the first item of all the the selected items. 
        
        # Extracting Links (returns a list)
        links = response.css("tr.athing .titlelink::attr(href)").extract()

        # Extracting the Times of the posts (returns a list)
        times = response.css("td.subtext .age a::text").extract()

        # For convinience we declare the YcombinatorItem class as the item variable. 
        # Our items.py file contains three fields:- title, link and postage_time.
        item = YcombinatorItem()

        self.page += 1 # How many pages we have scraped thus far

        for i in range(len(titles)):
            item["title"] = titles[i],
            item["link"] = links[i],
            item["postage_time"] = times[i]
        
            # yield is a generator and it is used here to make sure that all the items are returned to their respective fields before continuing with the following ones.
            yield item


        # Handling pagination

        # Here in this site the next page is termed as "More" and the url is a relative url. To obtain an absolute url we import urllib.parse and use the urljoin() method.

        next_page = urllib.parse.urljoin('https://news.ycombinator.com/jobs', response.css("a.morelink::attr(href)").get())    
    
        # Now we send a request to the next page url and we call the parse method on the received response. And, we stop the crawler after scraping first 3 pages.

        if self.page < 3:
            yield scrapy.Request(url=next_page, callback=self.parse)
        