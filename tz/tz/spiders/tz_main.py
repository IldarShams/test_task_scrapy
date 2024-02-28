import json
import scrapy
from scrapy import Request


class QuotesSpider(scrapy.Spider):
    name = "films"
    start_urls = [
        "https://www.scrapethissite.com/pages/ajax-javascript/"
    ]

    def parse(self, response):
        for year in response.xpath("//a[@class='year-link']"):  # Собираем года.
            yield Request(  # Ajax запрос на ресурс по годам.
                response.url + "?ajax=true&year=" + year.xpath("./text()").get(),
                callback=self.parse_query
            )

    def parse_query(self, response):  # Обработка ajax запроса.
        print(response.url)
        for d in json.loads(response.text):
            yield d
