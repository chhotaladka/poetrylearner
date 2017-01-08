import scrapy
import re
import json
import os, sys, traceback, time
from crawlers.spiders.base import BaseSpider

try:
    from crawlers.utils import save_to_db_poem, save_to_db_author, get_language_list_for_url
except ImportError:
    def save_to_db_poem(data):
        print data
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

    # DON'T CHANGE THE start_urls, all rules depend upon this page
    start_urls = ["http://www.kavitakosh.org/kk/%E0%A4%B0%E0%A4%9A%E0%A4%A8%E0%A4%BE%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8B%E0%A4%82_%E0%A4%95%E0%A5%80_%E0%A4%B8%E0%A5%82%E0%A4%9A%E0%A5%80"]
    # used to build the hrefs
    domain_name = "http://www.kavitakosh.org"
    
    # languages of the poetry to be crawled: hindi, urdu or english(default)
    # for this site, only hindi contents are worth crawling 
    LANGUAGES = ['hi',]
    
    LOGFILE = 'log_err_kangaroo.txt'
    
    # Number of articles/poetry saved to the database
    count = 0
    
    def parse(self, response):
        self.logger.info('KangarooBot got first response from %s', response.url)
        
        with open(self.LOGFILE, "a") as outfile:
            outfile.write("\n--------------------------------------------------\n")
            outfile.write("Spider name: %s\n"%(self.name))
            outfile.write("Start time: %s\n"%(time.asctime( time.localtime(time.time()) )))
            outfile.write("--------------------------------------------------\n")
            
        ######### TEST START #########
#         url = 'http://kavitakosh.org/kk/%E0%A4%9C%E0%A4%AF%E0%A4%B6%E0%A4%82%E0%A4%95%E0%A4%B0_%E0%A4%AA%E0%A5%8D%E0%A4%B0%E0%A4%B8%E0%A4%BE%E0%A4%A6'
#         self.logger.info('KangarooBot: test case 1')
#         yield scrapy.Request(url, callback=self.l2_parse_poet_page)
#         return
#         url = 'http://www.kavitakosh.org/kk/%E0%A4%AE%E0%A4%A8_%E0%A4%B2%E0%A4%BE%E0%A4%97%E0%A5%8D%E0%A4%AF%E0%A5%8B_%E0%A4%AE%E0%A5%87%E0%A4%B0%E0%A5%8B_%E0%A4%AF%E0%A4%BE%E0%A4%B0_%E0%A4%AB%E0%A4%BC%E0%A4%95%E0%A5%80%E0%A4%B0%E0%A5%80_%E0%A4%AE%E0%A5%87%E0%A4%82_/_%E0%A4%95%E0%A4%AC%E0%A5%80%E0%A4%B0'
#         self.logger.info('KangarooBot: test case 2')
#         yield scrapy.Request(url, callback=self.l3_parse_poetry_page)
#         return
        ######### TEST END #########
        
        links = response.xpath("//div[@id='mw-content-text']//div[@class='poet-list-section']//ul//li//a/@href").extract()
        author_links = [self.domain_name+x for x in links]
        
        for url in author_links:
            self.logger.debug("Visiting poet's URL : %s", url)
            yield scrapy.Request(url, callback=self.l2_parse_poet_page)
    
    
    def l2_parse_poetry_list(self, response):
        '''
        Find out the poetry/journal list, generate request for each item.
        '''
        self.logger.debug("l2_parse_poetry_list: extracting poem/journal links.")
        try:
            articles = response.xpath("//div[@id='mw-content-text']/ul/li//a/@href").extract()
            
        except:
            print("ERROR: l2_parse_poetry_list: ", sys.exc_info()[0])
            _trace = ''
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                print ("ERROR: error in %s on line %d" % (fname, lineno))
                _trace = _trace + "error in %s on line %d" % (fname, lineno)
            with open(self.LOGFILE, "a") as outfile:
                t = time.asctime( time.localtime(time.time()) )
                json.dump({'link': response.url, 'error': 'parsing poetry list failed', 'trace': _trace, 'time': t}, outfile, indent=4)
        
        articles_links = [self.domain_name + x for x in articles]
        for url in articles_links:
            # Check if the entry for ``url`` exist in db,
            # Also find out the list of languages in which the content is there.
            lang_list = get_language_list_for_url(url)
            # Now crawl poetry page only for remaining langauge
            for lang in (x for x in self.LANGUAGES if x not in lang_list):
                yield scrapy.Request(url, callback=self.l3_parse_poetry_page)
    
    
    def l2_parse_poet_page(self, response):
        '''
        Parse the poet page
        1. Extract Date of birth and date of death
        2. Extract year of birth and death
        3. Save Poet details
        4. Crawl further to scrap his/her articles
        '''
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
        
        except:
            self.logger.error("l2_parse_poet_page: %s", sys.exc_info()[0])
            _trace = ''
            for frame in traceback.extract_tb(sys.exc_info()[2]):
                fname,lineno,fn,text = frame
                self.logger.error("error in %s on line %d" % (fname, lineno))
                _trace = _trace + "error in %s on line %d" % (fname, lineno)
            with open(self.LOGFILE, "a") as outfile:
                t = time.asctime( time.localtime(time.time()) )
                json.dump({'link': response.url, 'error': 'parsing poet failed', 'trace': _trace, 'time': t}, outfile, indent=4)
        
        # Process the page for poetry/journal list
        return self.l2_parse_poetry_list(response)
    
    
    def l3_parse_poetry_page(self,response):
        """
        First check for the page containing div[@class='poem'] in the XPATH
        1. If found then extract the poem and save in the database
        2. If not found call l2_parse_poetry_list because it contains list of poems/journal
        """
        self.logger.debug("l3_parse_poetry_page: IN. %s", self.count)
        self.count = self.count + 1
        flag_list_found = False
        
        try:
            p = response.xpath("//div[@id='mw-content-text']/div[@class='poem']//p").extract()
            if len(p) is 0:
                # in some pages, the poetry is not in div[@class='poem']
                # e.g. http://www.kavitakosh.org/kk/%E0%A4%AE%E0%A4%A8_%E0%A4%B2%E0%A4%BE%E0%A4%97%E0%A5%8D%E0%A4%AF%E0%A5%8B_%E0%A4%AE%E0%A5%87%E0%A4%B0%E0%A5%8B_%E0%A4%AF%E0%A4%BE%E0%A4%B0_%E0%A4%AB%E0%A4%BC%E0%A4%95%E0%A5%80%E0%A4%B0%E0%A5%80_%E0%A4%AE%E0%A5%87%E0%A4%82_/_%E0%A4%95%E0%A4%AC%E0%A5%80%E0%A4%B0
                p = response.xpath("//div[@id='mw-content-text']//p").extract()
                if len(p) <= 1:
                    # it means that this page may contain poem/journal list
                    flag_list_found = True
            
            poem = " ".join(x.encode('utf-8') for x in p)
            
        except:
            self.logger.error("l3_parse_poetry_page: xpath error.")
            flag_list_found = True
        
        if (flag_list_found):
            # It may contains list of poems in a journal
            # Extract journal links from the page and generate request for each journal link
            self.logger.info('journal found')
            return self.l2_parse_poetry_list(response)
        
        # This is poetry page, extract the poetry
        try:
            h1 = response.xpath("//h1[@id='firstHeading']//text()").extract()[0].encode('utf-8')
            h1_list = h1.split('/')
            title = '/'.join(h1_list[:-1])
            poet = h1_list[-1]
            
            data = {}
            data['poem'] = poem
            data['url'] = response.url.encode('utf-8')
            data['title'] = title
            data['author'] = poet.strip()
            data['language'] = 'hi'# Content of this site are in hindi
            
            # Store these information in DB
            save_to_db_poem(data)

        except:
            self.logger.error("l3_parse_poetry_page: %s", sys.exc_info()[0])
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