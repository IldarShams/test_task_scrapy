import scrapy


class LoginSpider(scrapy.Spider):
    name = "new_york"
    start_urls = [
        "https://www.scrapethissite.com/pages/forms/"
    ]

    def parse(self, response):
        yield scrapy.FormRequest.from_response(                         # Запрос с заполнением формы.
            response,
            formdata={"q": "New York"},
            callback=self.parse_query,
        )

    def parse_query(self, response):
        for plink in response.xpath("//ul[@class='pagination']//a"):
            yield scrapy.Request(                                       # Проходим по страницам и формируем запросы.
                url=response.urljoin(plink.xpath("./@href").get()),     # К запросу добавляем номер страницы.
                callback=self.result_cb
            )

    def result_cb(self, response):                                          # Обработка по страницам.
        for team in response.xpath("//tr[@class='team']"):                  # Выбираем данные
            tm = team.xpath("./td[@class='name']/text()").get()
            year = team.xpath("./td[@class='year']/text()").get()
            wins = team.xpath("./td[@class='wins']/text()").get()
            losses = team.xpath("./td[@class='losses']/text()").get()
            ot_losses = team.xpath("./td[@class='ot-losses']/text()").get()
            win_perc = team.xpath("./td[@class='pct text-danger']/text()").get()
            gf = team.xpath("./td[@class='gf']/text()").get()
            ga = team.xpath("./td[@class='ga']/text()").get()
            plus_minus = team.xpath("./td[@class='diff text-danger']/text()").get()
            yield {                                                         # Возвращаем результат
                "Team Name": tm.strip() if tm is not None else tm,          # Убираем пробелы и новые строки, юзая strip
                "Year": year.strip() if year is not None else year,         # И делаем проверку на None.
                "Wins": wins.strip() if wins is not None else wins,
                "Losses": losses.strip() if losses is not None else losses,
                "OT Losses": ot_losses.strip() if ot_losses is not None else ot_losses,
                "Win %": win_perc.strip() if win_perc is not None else win_perc,
                "Goals For (GF)": gf.strip() if gf is not None else gf,
                "Goals Against (GA)": ga.strip() if ga is not None else ga,
                "+/-": plus_minus.strip() if plus_minus is not None else plus_minus
            }
