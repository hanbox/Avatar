# -*- coding: utf-8 -*-
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "jokes"

    def start_requests(self):
        urls = [
            'http://www.pengfu.com/xiaohua_1.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for joke in response.css('div.list-item'):
            yield {
                'title': joke.css('h1.dp-b a::text').extract_first(),
                'image_paths':[],
                'data': joke.css("div.content-img::text").extract_first().strip(),
                'src_url': response.url,
                'data_type': self.name,
            }

        # next_page = response.css('div.page div a.on::attr(href)').extract()
        # if len(next_page) > 1:
        #     next_page = next_page[1]
        # else:
        #     next_page = next_page[0]
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)