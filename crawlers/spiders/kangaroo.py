import scrapy
import re
import json
import os, sys, traceback, time
from crawlers.spiders.base import BaseSpider

try:
    from crawlers.utils import save_to_db_poem, save_to_db_author, get_language_list_for_url
except ImportError:
    def save_to_db_poem(data):
        print data['title']
        pass
    
    def save_to_db_author(data):
        print data
        pass
    
    def get_language_list_for_url(url):
        return []


class KangarooBot(scrapy.Spider):
    '''
    @sumamry: spider bot for the kavitakosh.
    
    > starts crwaling from the "rachanaakaaro.n kee soochee" page, i.e. list of poets page.
    > select the poets, save the poet if required.
    > crawl selected poets' creations till the poem page.
    > save the extracted poem.
    '''

    name = 'kavitakosh'
    allowed_domains = ['kavitakosh.org']

    # used to build the hrefs
    domain_name = "http://www.kavitakosh.org"
    
    # Home page. http://www.kavitakosh.org is giving 301
    home_url = 'http://kavitakosh.org/kk/%E0%A4%95%E0%A4%B5%E0%A4%BF%E0%A4%A4%E0%A4%BE_%E0%A4%95%E0%A5%8B%E0%A4%B6_%E0%A4%AE%E0%A5%81%E0%A4%96%E0%A4%AA%E0%A5%83%E0%A4%B7%E0%A5%8D%E0%A4%A0'

    # Start url
    start_urls = [home_url,]

    # DON'T CHANGE THE poet_list_url, all rules depend upon this page
    poet_list_url = "http://www.kavitakosh.org/kk/%E0%A4%B0%E0%A4%9A%E0%A4%A8%E0%A4%BE%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8B%E0%A4%82_%E0%A4%95%E0%A5%80_%E0%A4%B8%E0%A5%82%E0%A4%9A%E0%A5%80"

    # languages of the poetry to be crawled: hindi, urdu or english(default)
    # for this site, only hindi contents are worth crawling
    LANGUAGES = ['hi',]
    
    LOGFILE = 'log_err_kangaroo.txt'

    # Testcase number. Change here to run a testcase.
    TESTCASE = 0


    def parse(self, response):
        self.logger.info('KangarooBot got first response from %s', response.url)
        
        with open(self.LOGFILE, "a") as outfile:
            outfile.write("\n--------------------------------------------------\n")
            outfile.write("Spider name: %s\n"%(self.name))
            outfile.write("Start time: %s\n"%(time.asctime( time.localtime(time.time()) )))
            outfile.write("--------------------------------------------------\n")
            
        # Run testcase, if there is a `TESTCASE`
        if self.TESTCASE != 0:
            yield scrapy.Request(self.home_url, callback=self.run_testcase)
        else:
            # Start main crawler
            yield scrapy.Request(self.poet_list_url, callback=self.parse_poet_list)


    def run_testcase(self, response):
        '''
        @summary: Run `TESTCASE` number
        '''
        testcase = self.TESTCASE
        self.logger.info('running testcase %s.' % testcase)
        
        if testcase == 1:
            self.logger.info('testcase <Man lagyo yaar... by Kabir.>')
            url = 'http://www.kavitakosh.org/kk/%E0%A4%AE%E0%A4%A8_%E0%A4%B2%E0%A4%BE%E0%A4%97%E0%A5%8D%E0%A4%AF%E0%A5%8B_%E0%A4%AE%E0%A5%87%E0%A4%B0%E0%A5%8B_%E0%A4%AF%E0%A4%BE%E0%A4%B0_%E0%A4%AB%E0%A4%BC%E0%A4%95%E0%A5%80%E0%A4%B0%E0%A5%80_%E0%A4%AE%E0%A5%87%E0%A4%82_/_%E0%A4%95%E0%A4%AC%E0%A5%80%E0%A4%B0'
            yield scrapy.Request(url, callback=self.parse_poetry_page)
            
        elif testcase == 2:
            self.logger.info('testcase <Jaishankar Prasad>.')
            url = 'http://kavitakosh.org/kk/%E0%A4%9C%E0%A4%AF%E0%A4%B6%E0%A4%82%E0%A4%95%E0%A4%B0_%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%B8%E0%A4%BE%E0%A4%A6'
            yield scrapy.Request(url, callback=self.parse_poet_page)
            
        elif testcase == 3:
            self.logger.info('testcase <Kaka Hathrasi>.')
            url = 'http://www.kavitakosh.org/kk/%E0%A4%95%E0%A4%BE%E0%A4%95%E0%A4%BE_%E0%A4%B9%E0%A4%BE%E0%A4%A5%E0%A4%B0%E0%A4%B8%E0%A5%80'
            yield scrapy.Request(url, callback=self.parse_poet_page)
            
        elif testcase == 4:
            self.logger.info('testcase <Kaka tarang by Kaka Hathrasi>.')
            url = 'http://www.kavitakosh.org/kk/%E0%A4%95%E0%A4%BE%E0%A4%95%E0%A4%BE_%E0%A4%A4%E0%A4%B0%E0%A4%82%E0%A4%97_/_%E0%A4%95%E0%A4%BE%E0%A4%95%E0%A4%BE_%E0%A4%B9%E0%A4%BE%E0%A4%A5%E0%A4%B0%E0%A4%B8%E0%A5%80'
            yield scrapy.Request(url, callback=self.parse_poetry_page)
            
        elif testcase == 5:
            self.logger.info('testcase <Yama by Mahadevi Varma>.')
            url = 'http://kavitakosh.org/kk/%E0%A4%AF%E0%A4%BE%E0%A4%AE%E0%A4%BE_/_%E0%A4%AE%E0%A4%B9%E0%A4%BE%E0%A4%A6%E0%A5%87%E0%A4%B5%E0%A5%80_%E0%A4%B5%E0%A4%B0%E0%A5%8D%E0%A4%AE%E0%A4%BE'
            yield scrapy.Request(url, callback=self.parse_poetry_page)
            
        else:
            self.logger.info('invalid testcase discarded.')
            return


    def parse_poet_list(self, response):
        '''
        Start parsing from the poet list page to the poetry pages.
        '''
        links = response.xpath("//div[@id='mw-content-text']//div[@class='poet-list-section']//ul//li//a/@href").extract()
        author_links = [self.domain_name+x for x in links]
        
        for url in author_links:
            self.logger.debug("Visiting poet's URL : %s", url)
            yield scrapy.Request(url, callback=self.parse_poet_page)


    def parse_url_list(self, response):
        '''
        Find out the poem/collections/book list, generate request for each item.
        '''
        self.logger.debug("parse_url_list: extracting poem/collections links.")
        self.crawler.stats.inc_value('kangaroo/list_page_visit')
        
        try:
            # All URLs in main body content div i.e. mw-content-text
            urls_all = response.xpath("//div[@id='mw-content-text']//a/@href").extract()
            urls_all = set(urls_all)
            #print len(urls_all)
            
            # Exclude the URLs present in breadcrumbs
            urls_exclude = response.xpath("//div[@id='mw-content-text']//div[@id='kkrachna' or @class='kkrachna' or @id='extrainfobox']//a/@href").extract()
            urls_exclude = set(urls_exclude)
            #print len(urls_exclude)
            
            urls = urls_all - urls_exclude
            self.logger.debug("parse_url_list: %s urls found."%len(urls))
            
        except:
            print("ERROR: parse_url_list: ", sys.exc_info()[0])
            _trace = ''
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print ("ERROR: error in %s on line %d" % (fname, lineno))
                _trace = _trace + "error in %s on line %d" % (fname, lineno)
            with open(self.LOGFILE, "a") as outfile:
                t = time.asctime( time.localtime(time.time()) )
                json.dump({'link': response.url, 'error': 'parse_url_list failed', 'trace': _trace, 'time': t}, outfile, indent=4)

        urls = [self.domain_name + x for x in urls]
        
        for url in urls:
            # Check if the entry for ``url`` exist in db,
            # Also find out the list of languages in which the content is there.
            lang_list = get_language_list_for_url(url)
            # Now crawl poetry page only for remaining langauge
            for lang in (x for x in self.LANGUAGES if x not in lang_list):
                yield scrapy.Request(url, callback=self.parse_poetry_page)


    def parse_poet_page(self, response):
        '''
        Parse the poet page
        1. Extract Date of birth and date of death
        2. Extract year of birth and death
        3. Save Poet details
        4. Crawl further to scrap his/her articles
        '''
        self.crawler.stats.inc_value('kangaroo/poet_page_visit')
        
        try:
            name = response.xpath("//h1[@id='firstHeading']//text()").extract()[0]
            try:
                birth = response.xpath("//div[@id='mw-content-text']/table[@id='kkparichay-box']//div[@id='kkparichay-dob']/text()").extract()[0]
            except:
                birth = None
            try:
                death = response.xpath("//div[@id='mw-content-text']/table[@id='kkparichay-box']//div[@id='kkparichay-dod']/text()").extract()[0]
            except:
                death = None
                
            data = {}
            data['name'] = name
            data['birth'] = birth
            data['death'] = death
            data['url'] = response.url.encode('utf-8')
            
            # Store these information in DB
            save_to_db_author(data)
            self.crawler.stats.inc_value('kangaroo/poet_found')
            
        except:
            self.logger.error("parse_poet_page: %s", sys.exc_info()[0])
            _trace = ''
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                self.logger.error("error in %s on line %d" % (fname, lineno))
                _trace = _trace + "error in %s on line %d" % (fname, lineno)
            with open(self.LOGFILE, "a") as outfile:
                t = time.asctime( time.localtime(time.time()) )
                json.dump({'link': response.url, 'error': 'parsing poet failed', 'trace': _trace, 'time': t}, outfile, indent=4)
                
        # Process the page for poems/collections list
        return self.parse_url_list(response)


    def parse_poetry_page(self,response):
        """
        Parse the poetry page
        1. First check if the page contains a poetry or not.
        2. If Poetry not found, call parse_url_list because it may contain list of poems/collections/books.
        3. If Poetry found, then extract the poem and save in the database.
        """
        self.logger.debug("parse_poetry_page: IN.")
        self.crawler.stats.inc_value('kangaroo/poetry_page_visit')
        flag_poetry_found = True
        
        ##
        # Find out if the page contains a Poetry
        try:
            p = response.xpath("//div[@id='mw-content-text']/div[@class='poem']//p").extract()
            if len(p) is 0:
                # in some pages, the poetry is not in div[@class='poem']
                # e.g. http://www.kavitakosh.org/kk/%E0%A4%AE%E0%A4%A8_%E0%A4%B2%E0%A4%BE%E0%A4%97%E0%A5%8D%E0%A4%AF%E0%A5%8B_%E0%A4%AE%E0%A5%87%E0%A4%B0%E0%A5%8B_%E0%A4%AF%E0%A4%BE%E0%A4%B0_%E0%A4%AB%E0%A4%BC%E0%A4%95%E0%A5%80%E0%A4%B0%E0%A5%80_%E0%A4%AE%E0%A5%87%E0%A4%82_/_%E0%A4%95%E0%A4%AC%E0%A5%80%E0%A4%B0
                p = response.xpath("//div[@id='mw-content-text']//p").extract()
                
                if len(p):
                    # Now check for the length of the text under the <p>
                    # Because it may contains empty <p>, or one line text stating poetry is not available etc.
                    # Here we assume that the length of Poetry should be greater than 8.
                    p_t = response.xpath("//div[@id='mw-content-text']//p/text()").extract()
                    p_t = "".join(x.encode('utf-8') for x in p_t)
                    if len(p_t) <= 8:
                        flag_poetry_found = Flase
                else:
                    flag_poetry_found = Flase
        except:
            self.logger.error("parse_poetry_page: xpath error.")
            flag_poetry_found = False
            
        ##
        # If poetry not found...
        if (flag_poetry_found is False):
            # It may contains list of poems/collections/books
            self.logger.info('parse_poetry_page: no poetry found on this page.')
            return self.parse_url_list(response)
        
        ##
        # If Poetry found...
        # This is poetry page, extract the poetry
        try:
            h1 = response.xpath("//h1[@id='firstHeading']//text()").extract()[0].encode('utf-8')
            h1_list = h1.split('/')
            title = '/'.join(h1_list[:-1])
            poet = h1_list[-1]
            # Process and create Poetry
            poem = " ".join(x.encode('utf-8') for x in p)
            
            data = {}
            data['poem'] = poem
            data['url'] = response.url.encode('utf-8')
            data['title'] = title
            data['author'] = poet.strip()
            data['language'] = 'hi'# Content of this site are in hindi
            
            # Store these information in DB
            save_to_db_poem(data)
            self.crawler.stats.inc_value('kangaroo/poetry_found')
            
        except:
            self.logger.error("parse_poetry_page: %s", sys.exc_info()[0])
            _trace = ''
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                self.logger.error("error in %s on line %d" % (fname, lineno))
                _trace = _trace + "error in %s on line %d" % (fname, lineno)
            with open(self.LOGFILE, "a") as outfile:
                t = time.asctime( time.localtime(time.time()) )
                json.dump({'link': response.url, 'error': 'parsing poetry failed', 'trace': _trace, 'time': t}, outfile, indent=4)


class SpiderKangaroo(BaseSpider):
    '''
    @summary: Class to manage KangarooBot
    '''
    spider_name = "kangaroo"
    bot = KangarooBot

