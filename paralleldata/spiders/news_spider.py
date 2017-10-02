import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.spiders import Rule

class Page_ID(scrapy.Item):
    number = scrapy.Field()

class Page_URL(scrapy.Item):
    url = scrapy.Field()

class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["http://bianet.org/english/politics/", "http://bianet.org/english/people/", "http://bianet.org/english/law/", "http://bianet.org/english/human-rights/", "http://bianet.org/english/women/", "http://bianet.org/english/media/", "http://bianet.org/english/environment/", "http://bianet.org/english/society/", "http://bianet.org/english/art/", "http://bianet.org/english/sports/", "http://bianet.org/english/culture/"]
    start_urls = ["http://bianet.org/english/haberler?page="]
    
    def start_requests(self):
        # Starts crawling from the home page and iterates through the page numbers. Modify range of loop to change the last page to open (currenly from page 1 to 2.)
        for i in range(1,2):
            url = self.start_urls[0] + str(i)
            yield scrapy.Request(url, callback=self.parse_url)

    def parse_url(self, response):
        sel = Selector(response)
        all_links = sel.xpath('*//a/@href').extract()
        for link in all_links:
            main = "http://bianet.org"
            full_link = main + link
            for allowed_domain in self.allowed_domains:
                if allowed_domain in full_link:
                    print(full_link)
                    yield scrapy.Request(url=full_link, callback=self.parse_page1, dont_filter=True)


    def parse_page1(self, response):
        # Save the English page
        page_en = response.url.split("/")[-1]
        print(page_en)
        article_id = page_en.split("-")[0]
        filename_en = 'crawledsites/%s-en.html' %article_id
        
        hxs = Selector(response)
        text = hxs.select('//div[@class="article"]//text()').extract()
        links = hxs.select('//div[@class="article"]/p/em/a/@href').extract()
        id = Page_ID()
        id['number'] = article_id


        for link in links:
            with open(filename_en, 'w') as f:
                f.writelines(text)
                self.log('Saved file ')

            if 'kurdi' in link:
                # Go to the Kurdish link
                request = scrapy.Request(url=link, callback=self.parse_page3, dont_filter=True)
                request.meta['id'] = id['number']
                yield request
            else:
                # Go to the Turkish link
                request = scrapy.Request(url=link, callback=self.parse_page2, dont_filter=True)
                request.meta['id'] = id['number']
                yield request


    def parse_page2(self, response):
        # Save the Turkish translation
        page_tr = response.url.split("/")[-1]
        page_id = response.meta['id']
        htr = Selector(response)
        texttr = htr.select('//div[@class="article"]//text()').extract()
        filename_tr = 'crawledsites/%s-tr.html' %page_id
        with open(filename_tr, 'w') as f:
            f.writelines(texttr)
        self.log('Saved file ')

    def parse_page3(self, response):
        # Save the Kurdish translation
        page_kr = response.url.split("/")[-1]
        page_id = response.meta['id']
        hkr = Selector(response)
        textkr = hkr.select('//div[@class="article"]//text()').extract()
        filename_kr = 'crawledsites/%s-kr.html' %page_id
        with open(filename_kr, 'w') as f:
            f.writelines(textkr)
        self.log('Saved file ')
