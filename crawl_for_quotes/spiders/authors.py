import scrapy


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_URI": "authors.json",
        "FEED_EXPORT_ENCODING": "utf-8",
    }
    previous_links = set()

    def parse(self, response):
        target = "(about)"
        xpath_expression = f'//a[text()="{target}"]/@href'
        for about_link in response.xpath(xpath_expression).getall():
            yield scrapy.Request(
                url=self.start_urls[0] + about_link, callback=self.parse_about
            )
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link and next_link not in self.previous_links:
            self.previous_links.add(next_link)
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_about(self, response):
        for author in response.xpath("/html//div[@class='author-details']"):
            xpath_exp1 = "h3[@class='author-title']/text()"
            xpath_exp2 = "p/span[@class='author-born-date']/text()"
            xpath_exp3 = "p/span[@class='author-born-location']/text()"
            xpath_exp4 = "div[@class='author-description']/text()"
            yield {
                "fullname": author.xpath(xpath_exp1).get(),
                "born_date": author.xpath(xpath_exp2).get(),
                "born_location": author.xpath(xpath_exp3).get(),
                "description": author.xpath(xpath_exp4).get().strip(),
            }
