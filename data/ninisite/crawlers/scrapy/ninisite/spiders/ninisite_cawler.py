import scrapy
from ninisite.items import NinisiteItem
from functools import partial

class NinisiteCawlerSpider(scrapy.Spider):
    name = 'ninisite_cawler'
    
    def start_requests(self):
        url = 'https://www.ninisite.com/discussion'
        
        yield scrapy.Request(url=url, callback=self.get_categs)
            
    def get_categs(self, response):
        all_categs = response.xpath("//div[contains(@class,'category--header')]//a[@class='category--title']/@href").getall()
        
        yield from response.follow_all(all_categs,callback=self.get_topics)
        
    def get_topics(self, response):
        all_topics = response.xpath("//div[contains(@class,'category--header')]//h2[contains(@class,'topic--title')]/../@href").getall()
        
        yield from response.follow_all(all_topics,callback=self.parse)
        
        next_page = response.xpath("//a[@title='Next page']/@href").get()
        if next_page is not None:
            yield response.follow(next_page,callback=self.get_topics)
    
    def parse(self,response):
        topic = response.xpath("//h1[@itemprop='headline']/a/text()").get()
        if topic is None :
            self.logger.error(f"topic in {response.url} is None")
        else:
            topic = topic.strip()
        
        main_question = response.xpath("//article[@id='topic']//div[contains(@class,'post-message')]/p/text()").getall()
        main_question = list(map(lambda x:x.strip(),main_question))
        
        articles = response.xpath("//div[@id='posts']/article")
        
        get_article_info = partial(self.get_article_info,main_question, topic)
        items = map(get_article_info,articles)
        for item in items :
            yield item
        
        
    def get_article_info(self,main_question,topic,article_selector):
        answer = article_selector.xpath(".//div[contains(@class,'post-message')]/p/text()").getall()
        answer = list(map(lambda x:x.strip(),answer))
        
        reply_selector = article_selector.xpath(".//div[@class='reply-message']")
        if len(reply_selector) != 0:
            question_text = reply_selector.xpath("./text()").get().strip()
            if len(question_text) > 90:
                question_id = reply_selector.attrib['data-id']
                
                question_text = article_selector.xpath(f"//article[@id='post-{question_id}']//div[contains(@class,'post-message')]/p/text()").getall()
                question_text = list(map(lambda x:x.strip(),question_text))
        else:
            question_text = main_question
        
        return NinisiteItem(topic,question_text , answer)