import scrapy
from thuvienluat.items import DataItem


class DataSpider(scrapy.Spider):
    name = "data"
    allowed_domains = ["thuvienphapluat.vn"]
    page_number = 2
    start_urls = ["https://thuvienphapluat.vn/phap-luat/trach-nhiem-hinh-su"]

    custom_settings = {
        'FEEDS' : {
            'datathuvien.json' : {'format' : 'json', 'overwrite' : True}
        }
        
        # 'FEEDS': { 'data/%(name)s_%(time)s.csv': { 'format': 'csv',}}
        
    }

    def parse(self, response):
        cards = response.css('article.news-card')
        for card in cards:
            card_url = card.css('a.title-link::attr(href)').get()
            if card_url is not None:
                data_url = 'https://thuvienphapluat.vn' + card_url
            yield response.follow(data_url, callback= self.parse_page)

        next_page_url = 'https://thuvienphapluat.vn/phap-luat/trach-nhiem-hinh-su?page=' + str(DataSpider.page_number)
        if DataSpider.page_number < 185:
            DataSpider.page_number += 1
            yield response.follow(next_page_url, callback= self.parse)

    def parse_page(self, response):
        block = response.css('article div.row > div.col-md-9')
        content = block.css('section.news-content')
        item = DataItem()

        h2s = content.xpath('//h2')
        h2_text = []
        paragraph = []
        for i in range(len(h2s)):
            h2_text.append(h2s[i].xpath('.//text()').get())
            tags = h2s[i].xpath('./following-sibling::*[self::p or self::blockquote//em or self::p//a or self::p//span][count(preceding-sibling::h2) = $index + 1]', index=i)

            texts = []
            for tag in tags:
                tag_text = ''.join(tag.xpath('.//text()').extract())
                texts.append(tag_text)

            paragraph.append(' '.join(str(item) if item is not None else '' for item in texts))


        item['url'] = response.url,
        item['title'] = block.css('header h1.title::text').get(),
        item['h2_title'] = h2_text,
        item['paragraph'] = paragraph

        yield item
        
        