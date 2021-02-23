import scrapy


class LegoSpider(scrapy.Spider):
    name = "lego_scraper"

    # Set the User-Agent to Win10 pc with Chrome 88
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.182 Safari/537.36 '
    }

    set_count = 0

    def start_requests(self):
        url = "http://brickset.com/sets/year-2016"
        yield scrapy.http.Request(url, headers=self.headers)  # Just yields once, can be used for more URL's

    def parse(self, response):
        # Use CSS selector for getting set, and subsequent name, pieces, minifigs, and image url
        SET_SELECTOR = ".set"
        NAME_SELECTOR = 'h1 ::text'
        PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
        MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
        # IMAGE_SELECTOR = 'img ::attr(src)'

        # CSS selector for getting URL of next page
        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'

        for brickset in response.css(SET_SELECTOR):
            self.set_count += 1  # Increment set count

            print("------- NEW SET -------")
            yield {
                'name': brickset.css(NAME_SELECTOR).extract_first(),
                'pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
                'minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
                # 'image': brickset.css(IMAGE_SELECTOR).extract_first(),
            }

            next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
            if next_page:
                yield scrapy.http.Request(
                    response.urljoin(next_page),
                    callback=self.parse,
                    headers=self.headers
                )
