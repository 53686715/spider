# -*- coding: utf-8 -*-
import scrapy
import re
from kantt.items import KanttItem


class KttSpider(scrapy.Spider):
    name = "ktt"
    # allowed_domains = ["http://www.kantiantang.com/"]
    tmp = raw_input("Input ktturl: ")
    tmpurl = 'http://www.kantiantang.com/'
    if tmp != '':
        tmpurl = tmpurl + 'tag/' + tmp
        print tmpurl
    print tmpurl
    start_urls = (tmpurl,)

    def parse(self, response):
        # print response.body

        item = KanttItem()
        selector = scrapy.Selector(response)
        movie = selector.xpath('//div[@class="col-md-8"]')
        nextug = selector.xpath('//ul[@class="pagination"]/li/a/@href').extract()
        mm = len(nextug) - 1
        nexturl = nextug[mm].replace('?', '/?')
        # print 'next:' + nexturl
        for each in movie:
            title1 = each.xpath('div[@class="page-header"]/h4/a/text()').extract()
            # title2 = each.xpath('div[@class="page-header"]/h4/small/a/text()').extract()
            url = each.xpath('div[@class="page-header"]/h4/a/@href').extract()
            rate = each.xpath('div[@class="row"]/div[@class="col-xs-6 col-md-3"]/div').extract()

            rate2 = []
            for x in rate:
                x = x.replace(' ', '').replace('\n', '')
                x = re.findall('</a>(.*?)</div>', x)
                rate2.append(x[0])
            rate = rate2
            for i in range(0, len(title1)):
                # print i, title1[i], title2[i], rate[i], url[i]
                item['title1'] = title1[i]
                # item['title2'] = title2[i]
                item['rate'] = rate[i]
                item['url'] = url[i]
                yield item
                # i = i + 1
            # print 'response:' + response.url
            # tmp = []
            # for j in range(0,3):
            #     j = j + 1
            #     xx = response.url + '?page='+str(j)
            #     yield scrapy.http.Request(xx, callback=self.parse)
            yield scrapy.http.Request(nexturl, callback=self.parse)
