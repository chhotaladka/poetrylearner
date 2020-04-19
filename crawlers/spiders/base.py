import scrapy
from scrapy.crawler import CrawlerProcess


class BaseSpider(object):
    '''
    @summary: Abstract Base class for Spiders
    '''
    spider_name = "foo"
    bot = None # spider bot Class, derive class of scrapy.Spider
    
    process = None # CrawlerProcess instance
    
    class Meta:
        abstract = True
    
    def __init__(self):
        # Check if `bot` is derived class of scrapy.Spider or not 
        if issubclass(self.bot, scrapy.Spider):
            self.process = CrawlerProcess({
                'BOT_NAME': 'majdoor',
                'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
                'RANDOMIZE_DOWNLOAD_DELAY': True,
                'COOKIES_ENABLED': False,
                'LOG_LEVEL': 'INFO',
                'DOWNLOAD_TIMEOUT': 20,
                'REDIRECT_ENABLED': False
            })
            self.process.crawl(self.bot)
        else:
            raise TypeError("bot is not a derived class of scrapy.Spider")
    
    
    def test(self):
        '''
        @summary: Tests for spider. Derived class would override this function.
        '''
        print('============= testing %s =============='%(self.spider_name))
        print('============== end of testing ===============')
    
    def resume(self):
        '''
        @summary: Resume/Run spider
        '''
        print('============= running %s =============='%(self.spider_name))
        
        self.process.start()
        
        print('================ end of run =================')