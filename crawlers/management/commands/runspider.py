from django.core.management.base import BaseCommand, CommandError
import sys
import traceback

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging

from crawlers.spiders.wiki import WikiBot

from crawlers.spiders.secret.kangaroo import KangarooBot
from crawlers.spiders.secret.umbrellabird import UmbrellabirdBot
from crawlers.spiders.secret.reindeer import ReindeerBot


class Command(BaseCommand):
    help = 'Start running spiders; OPTIONS: kangaroo/umbrellabird/reindeer'

    def add_arguments(self, parser):
        parser.add_argument('run', nargs='+', type=str)

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
        
        for run in options['run']:
            try:
                if run == "kangaroo":
                    process.crawl(KangarooBot)
                    flag = True
                elif run == "wiki":
                    process.crawl(WikiBot)
                    flag = True
                elif run == "umbrellabird":
                    process.crawl(UmbrellabirdBot)
                    flag = True
                elif run == "reindeer":
                    process.crawl(ReindeerBot)
                    flag = True                    
                else:
                    print ('ERROR: Command argument "%s" does not exist' % run)
                    
            except:
                print "Unexpected error:", sys.exc_info()[0]
                for frame in traceback.extract_tb(sys.exc_info()[2]):
                    fname,lineno,fn,text = frame
                    print "Error in %s on line %d" % (fname, lineno)
                raise CommandError('Command "%s" failed to execute' % run)
        
        # Start the spider if any match found
        if flag:
            process.start() # the script will block here until the crawling is finished