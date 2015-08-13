from scrapy.spiders import CrawlSpider, Rule
import re
from scrapy.selector import Selector
from douban.items import DoubanItem
from scrapy.linkextractors import LinkExtractor

class DoubanSpider(CrawlSpider):
    name = "douban_collect"

    rules = [Rule(LinkExtractor(allow=(r'\/collect\?start=\d+.*',)), follow=True, callback='parse_item')]
            
    def __init__(self, user_id):
        super(DoubanSpider, self).__init__()
        self.allowed_domains = ["movie.douban.com"]
        self.start_urls = ["http://movie.douban.com/people/%s/collect?start=0&sort=time&rating=all&filter=all&mode=grid"%user_id]



    def parse_item(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="grid-view"]/div[@class="item"]/div[@class="info"]/ul')
        items = []

        for site in sites:
            item = DoubanItem()
            # name
            item['name'] = site.xpath('.//li[@class="title"]/a/em/text()').extract()

            # intro
            item['intro'] = site.xpath('.//li[@class="intro"]/text()').extract()

            # tags
            item['tags'] = site.xpath('.//li[@class="tags"]/text()').extract()

            # url
            item['url'] = site.xpath('.//li[@class="title"]/a/@href').extract()

            # movie_id
            item['movie_id'] = re.search("http://movie.douban.com/subject/(?P<movie_id>\d+)", item['url'][0]).group(1)

            # date
            data = site.xpath('.//li/span[@class="date"]/text()').extract()
            m = re.compile('(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)')
            date = dict()
            date['year'] = m.search(data[0]).group(1)
            date['month'] = m.search(data[0]).group(2)
            date['day'] = m.search(data[0]).group(3)
            item['date'] = date
            items.append(item)

        return items

