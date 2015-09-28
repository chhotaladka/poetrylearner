from django.core.management.base import BaseCommand, CommandError
import sys
import traceback

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging

from crawlers.wiki_spider import WikiSpider
from crawlers.kk_spider import KavitakoshSpider
from crawlers.kk_author_spider import KavitakoshAuthorSpider
from crawlers.urdupoetry_spider import UrdupoetrySpider



class Command(BaseCommand):
    help = 'Start running spiders; OPTIONS: kk - kavitakosh; kk_auth; upoetry - urdupoetry'

    def add_arguments(self, parser):
        parser.add_argument('site', nargs='+', type=str)

    def handle(self, *args, **options):
        flag = False
        process = CrawlerProcess({
            'BOT_NAME': 'majdoor',
            'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
            'RANDOMIZE_DOWNLOAD_DELAY': True,
            'COOKIES_ENABLED': False,
            'LOG_LEVEL': 'INFO',
            'DOWNLOAD_TIMEOUT': 20,
            'REDIRECT_ENABLED': False
        })
        
        for site in options['site']:
            try:
                if site == "kk":
                    process.crawl(KavitakoshSpider)
                    flag = True
                elif site == "kk_auth":
                    process.crawl(KavitakoshAuthorSpider)
                    flag = True
                elif site == "wiki":
                    process.crawl(WikiSpider)
                    flag = True
                elif site == "upoetry":
                    process.crawl(UrdupoetrySpider)
                    flag = True
                else:
                    print ('ERROR: Command argument "%s" does not exist' % site)
                    
            except:
                print "Unexpected error:", sys.exc_info()[0]
                for frame in traceback.extract_tb(sys.exc_info()[2]):
                    fname,lineno,fn,text = frame
                    print "Error in %s on line %d" % (fname, lineno)
                raise CommandError('Command "%s" failed to execute' % site)
        
        # Start the spider if any match found
        if flag:
            process.start() # the script will block here until the crawling is finished