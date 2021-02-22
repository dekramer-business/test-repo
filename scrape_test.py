import scrapy


class LegoSpider(scrapy.Spider):
    name = "lego_scraper"

    def start_requests(self):
        url = "http://brickset.com/sets/year-2016"

        # Set the User-Agent to Win10 pc with Chrome 88
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/88.0.4324.182 Safari/537.36 '
        }
        yield scrapy.http.Request(url, headers=headers)  # Just yields once, can be used for more URL's

    def parse(self, response):
        SET_SELECTOR = ".set"
        for brickset in response.css(SET_SELECTOR):

            NAME_SELECTOR = 'h1 ::text'  # Use CSS selector for getting text in h1
            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            # IMAGE_SELECTOR = 'img ::attr(src)'
            print("------- NEW SET -------")
            yield {
                'name': brickset.css(NAME_SELECTOR).extract_first(),
                'pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
                'minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
                # 'image': brickset.css(IMAGE_SELECTOR).extract_first(),
            }