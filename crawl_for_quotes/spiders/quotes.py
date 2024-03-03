import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_URI": "quotes.json",
        "FEED_EXPORT_ENCODING": "utf-8",
    }
    previous_links = set()

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                "author": quote.xpath("span/small/text()").extract()[0],
                "quote": quote.xpath("span[@class='text']/text()").get(),
            }
            next_link = response.xpath("//li[@class='next']/a/@href").get()
            if next_link and next_link not in self.previous_links:
                self.previous_links.add(next_link)
                yield scrapy.Request(url=self.start_urls[0] + next_link)
