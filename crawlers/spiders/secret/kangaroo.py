import scrapy
import re
from datetime import datetime
import json

try:
    from crawlers.utils import save_to_db_poem, save_to_db_author, get_language_list_for_url
except ImportError:    
    def save_to_db_poem(data):
        print data
        
    def save_to_db_author(data):
        print data
        
    def get_language_list_for_url(url):
        print url


class KangarooBot(scrapy.Spider):
    """
    Crawl the kavitakosh pages.
    
    It starts crwaling from the "rachanaakaaro.n kee soochee" page, i.e. list of poets page.
    It select the poets with some rules (according to their Date of Birth/Death) to avoid the copyright issues. 
    Crawls selected poets' creations till the poem page, and finally save the extracted poem into
    the database i.e. crawlers.models.RawArticle

    """

    name = 'kavitakosh'
    allowed_domains = ['kavitakosh.org']
    """
    DON'T CHANGE THE start_urls, all rules depend upon this page
    """
    start_urls = ["http://www.kavitakosh.org/kk/%E0%A4%B0%E0%A4%9A%E0%A4%A8%E0%A4%BE%E0%A4%95%E0%A4%BE%E0%A4%B0%E0%A5%8B%E0%A4%82_%E0%A4%95%E0%A5%80_%E0%A4%B8%E0%A5%82%E0%A4%9A%E0%A5%80"]
    
    # used to build the hrefs
    domain_name = "http://www.kavitakosh.org"
    
    # languages of the poetry to be crawled: hindi, urdu or english(default)
    # for this site, only hindi contents are worth crawling 
    LANGUAGES = ['hi']
    
    def parse(self, response):

        links = response.xpath("//div[@id='mw-content-text']/table//td[2]//a/@href").extract()
        author_links = [self.domain_name+x for x in links]        
        
        for url in author_links:
            print "Visiting poet's URL : ", url
            yield scrapy.Request(url, callback=self.parse_author_page)        


    def parse_author_page(self, response):
        """
        Parse the author page
        1. Extract Date of birth and date of death
        2. Extract year of birth and death
        3. Save Author details
        4. Crawl further to scrap his/her articles
        """
        name = None                
        # date of birth
        birth = None
        # date of death
        death = None        

        try:
            name = response.xpath("//h1[@id='firstHeading']//text()").extract()[0]    
            #print name            
        except:
            print "################################## name error #####################"
        	
        try:
            birth = response.xpath("//div[@id='mw-content-text']/table[@id='kkparichay-box']//div[@id='kkparichay-dob']/text()").extract()[0]	
            #print dob            
        except:
            pass
        
        try:
            death = response.xpath("//div[@id='mw-content-text']/table[@id='kkparichay-box']//div[@id='kkparichay-dod']/text()").extract()[0]	
            #print dod            
        except:
            pass
        
           
        data = {}
        data['name'] = name
        data['birth'] = birth
        data['death'] = death
        data['url'] = response.url.encode('utf-8')
        
        # Store these information in DB
        save_to_db_author(data)

        ##
        # Parse the page, find out the articles list, generate request for each article
        # Extract article links from the Author page and generate request for each        
        try:
            print "DBG:: Extracting poem links from Author page"
            articles = response.xpath("//div[@id='mw-content-text']/ul/li/a/@href").extract()
    
            articles_links = [self.domain_name+x for x in articles]
            for url in articles_links:
                # Check if the entry for ``url`` exist in db,
                # Also find out the list of languages in which the content is there.
                lang_list = get_language_list_for_url(url)
                # Now crawl poetry page only for remaining langauge
                for lang in (x for x in self.LANGUAGES if x not in lang_list):                                  
                    #print "Visiting Article: ", url
                    yield scrapy.Request(url, callback=self.parse_article_page)
        except:
            print "Nothing found in Author page!!!"
        

    def parse_article_page(self,response):
        """
        First check for the page containing div[@class='poem'] in the XPATH
        1. If found then extract the poem and save in the database
        2. If not found call parse_author_page again because it contains list of poems in a journal 
        """
        try:
            print "Extracting poem from Article page"
            p = response.xpath("//div[@id='mw-content-text']/div[@class='poem']//p").extract()
            poem = " ".join(x.encode('utf-8') for x in p)
            try:
                h1 = response.xpath("//h1[@id='firstHeading']//text()").extract()[0].encode('utf-8')
                title = h1
                author = h1.split('/')[-1]                
                
                data = {}
                data['poem'] = poem
                data['url'] = response.url.encode('utf-8')        
                data['title'] = title
                data['author'] = author.title()                
                data['language'] = 'hi'# Content of this site are in hindi
                
                # Store these information in DB
                save_to_db_poem(data)

            except:
                print "Title not found"
        except:
            # Extract article links from the Author page and generate request for each            
            try:
                print "Extracting poem links from Author page"
                articles = response.xpath("//div[@id='mw-content-text']/ul/li/a/@href").extract()
        
                articles_links = [self.domain_name+x for x in articles]
                for url in articles_links:
                    # Check if the entry for ``url`` exist in db,
                    # Also find out the list of languages in which the content is there.
                    lang_list = get_language_list_for_url(url)                
                    # Now crawl poetry page only for remaining langauge
                    for lang in (x for x in self.LANGUAGES if x not in lang_list):                                  
                        #print "Visiting Article: ", url
                        yield scrapy.Request(url, callback=self.parse_article_page)
            except:
                print "Nothing found in Author page!!!"            