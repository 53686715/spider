# -*- coding: utf-8 -*-
import scrapy
import re
from zhihu.items import *


offset = 0
tmp = raw_input("Input keyword: ")
keyw = tmp
em = '<em>'
em2 = '</em>'
em3 = '<\\/em>'


class ZhSpider(scrapy.Spider):
    name = "zh"
    allowed_domains = ["zhihu.com"]
    start_urls = ('https://www.zhihu.com/r/search?q=' + keyw +
                  '&sort=upvote&correction=0&type=content&offset=' + offset.__str__(), )

    def parse(self, response):
        # print response.body
        item = ZhihuItem()
        nextp = re.findall('&offset=(.*?)"},', response.body)
        print nextp[0]
        h = response.body
        # zhuanlan
        zl = re.findall('item clearfix article-item.*?" href=\\\\\"(.*?)\\\\\" class=\\\\\"'
                        'js-title-link\\\\\">(.*?)<\\\/a><\\\/div>.*?data-bind-votecount>(.*?)'
                        '<\\\/a>', h)
        for each in zl:
            x = each[0].replace('\\', '')
            y = each[1].replace(em, '').replace(em2, '').replace(em3, '')\
                .decode("unicode_escape").encode("UTF-8")
            z = each[2]
            # print x, z, y
            item['url'] = x
            item['title'] = y
            item['zan'] = z
            yield item
        # question
        qs = re.findall('item clearfix\\\.*?question\\\/(.*?)\\\\\".*?js-title-link\\\\\">(.*?)<\\\/a>'
                        '.*?count\\\\\" data-bind-votecount>(.*?)<\\\/a>', h)
        for e2 in qs:
            x = 'https://www.zhihu.com/question/' + e2[0]
            y = e2[1].replace(em, '').replace(em2, '').replace(em3, '')\
                .decode("unicode_escape").encode("UTF-8")
            z = e2[2]
            # print x, z, y
            item['url'] = x
            item['title'] = y
            item['zan'] = z
            yield item
        if nextp[0]:
            n = 'https://www.zhihu.com/r/search?q=' + keyw + \
                   '&sort=upvote&correction=0&type=content&offset=' + nextp[0]
            yield scrapy.http.Request(n, callback=self.parse)
