import scrapy

from scrapy.http import Request

class PPTXDownloader(scrapy.Spider):
    name = 'pptx_downloader'
    start_urls = ['https://www.bing.com/search?q=filetype%3apptx+strategy&filters=ex1%3a%22ez5_18524_18889%22&qs=n&FORM=000017&sp=-1&pq=filetype%3appt+strategy&sc=0-21&cvid=5C53778DCE6D42CD884A658B1DAF0898']

    def parse(self, response):

        selector = '.b_algo h2 a::attr(href)'
        for href in response.css(selector).extract():
            self.logger.info('Requesting %s', href)
            yield Request(
                url=response.urljoin(href),
                callback=self.save_pptx
            )

        next_page_url = response.xpath("//a[contains(@class, 'sb_pagN')]/@href").extract_first()
        next_page_url = response.urljoin(next_page_url)
        self.logger.info('Next page url %s', next_page_url)
        if next_page_url:
            yield Request(next_page_url, callback=self.parse)

    def save_pptx(self, response):
        s = response.url.split('/')[-1]
        path = r"downloads\\" + "".join(x for x in s if x.isalnum()) + ".pptx"
        self.logger.info('Saving %s', path)
        with open(path, 'wb') as file:
            file.write(response.body)