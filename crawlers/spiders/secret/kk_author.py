import scrapy
import re
from datetime import datetime
from crawlers.save import save_to_db

class KavitakoshAuthorSpider(scrapy.Spider):
    """
    Crawl the kavitakosh page.
    It starts crwaling from the links of author pages. 
    Crawls all poets' creations till the poem page, and finally save the extracted poem into
    the database i.e. crawlers.models.RawArticle
    """

    name = 'kavitakosh'
    allowed_domains = ['kavitakosh.org']
    
    """
    DON'T CHANGE THE start_urls, all rules depend upon this page
    """
    start_urls = [
                    "http://www.kavitakosh.org/kk/%E0%A4%B6%E0%A5%8D%E0%A4%B0%E0%A5%80%E0%A4%AA%E0%A4%A4%E0%A4%BF", 
                    "http://www.kavitakosh.org/kk/%E0%A4%B9%E0%A4%B0%E0%A4%BF%E0%A4%A6%E0%A4%BE%E0%A4%B8", 
                    "http://www.kavitakosh.org/kk/%E0%A4%B8%E0%A5%8C%E0%A4%A6%E0%A4%BE", 
                    "http://www.kavitakosh.org/kk/%E0%A4%B8%E0%A5%87%E0%A4%A8%E0%A4%BE%E0%A4%AA%E0%A4%A4%E0%A4%BF", 
                    "http://www.kavitakosh.org/kk/%E0%A4%B8%E0%A5%81%E0%A4%AC%E0%A5%8D%E0%A4%B0%E0%A4%B9%E0%A5%8D%E0%A4%AE%E0%A4%A3%E0%A5%8D%E0%A4%AF%E0%A4%AE_%E0%A4%AD%E0%A4%BE%E0%A4%B0%E0%A4%A4%E0%A5%80", 
                    "http://www.kavitakosh.org/seemab", 
                    "http://www.kavitakosh.org/kk/%E0%A4%B8%E0%A4%B0%E0%A4%B9%E0%A4%AA%E0%A4%BE", 
                    "http://www.kavitakosh.org/kk/%E0%A4%B6%E0%A5%87%E0%A4%96_%E0%A4%95%E0%A4%BF%E0%A4%AB%E0%A4%BC%E0%A4%BE%E0%A4%AF%E0%A4%A4", 
                    "http://www.kavitakosh.org/kk/%E0%A4%B6%E0%A4%BE%E0%A4%B9_%E0%A4%B9%E0%A4%BE%E0%A4%A4%E0%A4%BF%E0%A4%AE", 
                    "http://www.kavitakosh.org/kk/%E0%A4%B6%E0%A4%BE%E0%A4%A6_%E0%A4%85%E0%A4%9C%E0%A4%BC%E0%A5%80%E0%A4%AE%E0%A4%BE%E0%A4%AC%E0%A4%BE%E0%A4%A6%E0%A5%80", 
                    "http://www.kavitakosh.org/kk/%E0%A4%B2%E0%A4%B2%E0%A4%BF%E0%A4%A4_%E0%A4%95%E0%A4%BF%E0%A4%B6%E0%A5%8B%E0%A4%B0%E0%A5%80", 
                    "http://www.kavitakosh.org/rahim", 
                    "http://www.kavitakosh.org/kk/%E0%A4%AE%E0%A5%81%E0%A4%AC%E0%A4%BE%E0%A4%B0%E0%A4%95", 
                    "http://www.kavitakosh.org/kk/%E0%A4%85%E0%A4%9A%E0%A4%B2_%E0%A4%95%E0%A4%B5%E0%A4%BF_(%E0%A4%85%E0%A4%9A%E0%A5%8D%E0%A4%AF%E0%A5%81%E0%A4%A4%E0%A4%BE%E0%A4%A8%E0%A4%82%E0%A4%A6)", 
                    "http://www.kavitakosh.org/kk/%E0%A4%AD%E0%A5%80%E0%A4%B7%E0%A4%A8%E0%A4%9C%E0%A5%80", 
                    "http://www.kavitakosh.org/kk/%E0%A4%AD%E0%A4%97%E0%A4%B5%E0%A4%A4%E0%A5%8D_%E0%A4%B0%E0%A4%B8%E0%A4%BF%E0%A4%95", 
                    "http://www.kavitakosh.org/kk/%E0%A4%AC%E0%A5%88%E0%A4%B0%E0%A5%80%E0%A4%B8%E0%A4%BE%E0%A4%B2", 
                    "http://www.kavitakosh.org/kk/%E0%A4%A8%E0%A5%87%E0%A4%B5%E0%A4%BE%E0%A4%9C%E0%A4%BC", 
                    "http://www.kavitakosh.org/kk/%E0%A4%A7%E0%A4%A8%E0%A5%80_%E0%A4%A7%E0%A4%B0%E0%A4%AE%E0%A4%A6%E0%A4%BE%E0%A4%B8", 
                    "http://www.kavitakosh.org/kk/%E0%A4%A7%E0%A4%A8%E0%A4%AA%E0%A4%BE%E0%A4%B2", 
                    "http://www.kavitakosh.org/kk/%E0%A4%A8%E0%A4%BE%E0%A4%B8%E0%A4%BF%E0%A4%96%E0%A4%BC", 
                    "http://www.kavitakosh.org/kk/%E0%A4%A6%E0%A4%BE%E0%A4%A6%E0%A5%82_%E0%A4%A6%E0%A4%AF%E0%A4%BE%E0%A4%B2", 
                    "http://www.kavitakosh.org/kk/%E0%A4%9C%E0%A4%97%E0%A4%A8%E0%A4%BF%E0%A4%95", 
                    "http://www.kavitakosh.org/kk/%E0%A4%9A%E0%A4%A4%E0%A5%81%E0%A4%B0%E0%A5%8D%E0%A4%AD%E0%A5%81%E0%A4%9C%E0%A4%A6%E0%A4%BE%E0%A4%B8", 
                    "http://www.kavitakosh.org/kk/%E0%A4%A6%E0%A5%80%E0%A4%A8", 
                    "http://www.kavitakosh.org/kk/%E0%A4%9B%E0%A5%80%E0%A4%A4%E0%A4%B8%E0%A5%8D%E0%A4%B5%E0%A4%BE%E0%A4%AE%E0%A5%80", 
                    "http://www.kavitakosh.org/kk/%E0%A4%9B%E0%A4%A4%E0%A5%8D%E0%A4%B0%E0%A4%A8%E0%A4%BE%E0%A4%A5", 
                    "http://www.kavitakosh.org/kk/%E0%A4%9A%E0%A4%B0%E0%A4%A3%E0%A4%A6%E0%A4%BE%E0%A4%B8", 
                    "http://www.kavitakosh.org/kk/%E0%A4%97%E0%A5%8B%E0%A4%B5%E0%A4%BF%E0%A4%A8%E0%A5%8D%E0%A4%A6", 
                    "http://www.kavitakosh.org/kk/%E0%A4%98%E0%A4%A8%E0%A4%BE%E0%A4%A8%E0%A4%82%E0%A4%A6", 
                    "http://www.kavitakosh.org/kk/%E0%A4%97%E0%A5%8B%E0%A4%B0%E0%A4%96%E0%A4%A8%E0%A4%BE%E0%A4%A5", 
                    "http://www.kavitakosh.org/kk/%E0%A4%97%E0%A4%BF%E0%A4%B0%E0%A4%BF%E0%A4%A7%E0%A4%B0", 
                    "http://www.kavitakosh.org/kk/%E0%A4%95%E0%A5%81%E0%A4%AE%E0%A5%8D%E0%A4%AD%E0%A4%A8%E0%A4%A6%E0%A4%BE%E0%A4%B8", 
                    "http://www.kavitakosh.org/kk/%E0%A4%95%E0%A4%BF%E0%A4%B6%E0%A5%8B%E0%A4%B0", 
                    "http://www.kavitakosh.org/kk/%E0%A4%95%E0%A5%83%E0%A4%B7%E0%A5%8D%E0%A4%A3%E0%A4%A6%E0%A4%BE%E0%A4%B8",
                    ]
    
    domain_name = "http://www.kavitakosh.org"
    count_parse_author = 0
    count_surl = 0
    count_dob = 0
    count_dod = 0
    count_valid = 0
    count_invalid_yr = 0
    count_articles= 0
    
    def parse(self, response):

        self.count_parse_author = self.count_parse_author + 1
        author_link = ''

        author_link = response.url
        
        print "Parsing author No. ", self.count_parse_author

        # Parse the page, find out the articles list, generate request for each article              
        try:
            print "Extracting poem links from Author page"
            articles = response.xpath("//div[@id='mw-content-text']/ul/li/a/@href").extract()

            articles_links = [self.domain_name+x for x in articles]
            for url in articles_links:
                print "visiting ARTICLE ", url
                yield scrapy.Request(url, callback=self.parse_article_page)
        except:
            print "Nothing found in Author page!!!"
            
      
        #yield { 'link': author_link }
        

    """
    First check for the page containing div[@class='poem'] in the XPATH
    1. If found then extract the poem.
    2. If not found call parse_author_page again because it contains list of poems in a journal 
    """
    def parse_article_page(self,response):
        try:
            print "Extracting poem from Article page"
            p = response.xpath("//div[@id='mw-content-text']/div[@class='poem']//p").extract()
            poem = " ".join(x.encode('utf-8') for x in p)

            try:
                h1 = response.xpath("//h1[@id='firstHeading']//text()").extract()[0].encode('utf-8')
                title = h1
                author = h1.split('/')[-1]
                
                self.count_articles = self.count_articles + 1
                
                data = {}
                data['index'] = self.count_articles
                data['title'] = title
                data['author'] = author
                data['poem'] = poem
                data['url'] = response.url.encode('utf-8')
                
                # Store these information in DB
                save_to_db(data)
                
            except:
                print "Title not found"
        except:
            try:
                print "Extracting poem links from Journal page"
                articles = response.xpath("//div[@id='mw-content-text']/ul/li/a/@href").extract()

                articles_links = [self.domain_name+x for x in articles]
                for url in articles_links:
                    print "visiting ARTICLE ", url
                    yield scrapy.Request(url, callback=self.parse_article_page)
            except:
                print "Nothing found in Author page!!!"
        
