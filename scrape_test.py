import scrapy


class LegoSpider(scrapy.Spider):
    name = "lego_scraper"
    start_urls = ['http://brickset.com/sets/year-2016']

    def start_requests(self):
        url = "http://brickset.com/sets/year-2016"

        # Set the headers here. The important part is "application/json"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
        }
        yield scrapy.http.Request(url, headers=headers)

    def parse(self, response):
        SET_SELECTOR = ".set"
        for brickset in response.css(SET_SELECTOR):

            NAME_SELECTOR = "h1 ::text"
            yield {
                'name': brickset.css(NAME_SELECTOR).extract_first(),
            }