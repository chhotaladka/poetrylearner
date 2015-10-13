"""
It is only for the refrence purpose.
Use the management commands instead of using it.
"""
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging

from crawlers.spiders.wiki import WikiSpider

process = CrawlerProcess({
    'BOT_NAME': 'majdoor',
    'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
    'RANDOMIZE_DOWNLOAD_DELAY': True,
    'COOKIES_ENABLED': False,
    'LOG_LEVEL': 'INFO',
    'DOWNLOAD_TIMEOUT': 20,
    'REDIRECT_ENABLED': False
})


process.crawl(WikiSpider)
#process.crawl('wikipedia', urls='https://en.wikipedia.org/wiki/Gulzar')
process.start() # the script will block here until the crawling is finished