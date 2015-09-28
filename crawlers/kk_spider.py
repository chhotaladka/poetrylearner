import scrapy
import re
from datetime import datetime
import json
from crawlers.save import save_to_db


class KavitakoshSpider(scrapy.Spider):
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
    
    count_parse_author = 0
    count_surl = 0
    count_dob = 0
    count_dod = 0
    count_valid = 0
    count_invalid_yr = 0
    count_articles= 0
    
    def parse(self, response):
        #print response.body

        links = response.xpath("//div[@id='mw-content-text']/table//td[2]//a/@href").extract()
        author_links = [self.domain_name+x for x in links]
        
        """
        # This file contains the entries regarding author died less than 60 year back or born after 1895 current year being 2015
        # Needs to be discarded
        """
        with open("KK_invalid_author.txt", "w") as outfile:
            outfile.write("------------------INVALID AUTHOR LIST--------------------------------\n")
        
        """
        # DOD or DOB not found or in invalid format
        # Manual extraction is required for this list
        """
        with open("KK_unknown_author.txt", "w") as outfile:
            outfile.write("------------------UNKNOWN AUTHOR LIST--------------------------------\n")

        
        for url in author_links:
            print "Visiting poet's URL : ", url
            yield scrapy.Request(url, callback=self.parse_author_page)
        


    def parse_author_page(self, response):
        """
        Parse the author page
        1. Extract Date of birth and date of death
        2. Find out the validity of the copyrights of his/her articles
        3. If valid, then crawl further to scrap his/her articles
        """
        
        self.count_parse_author = self.count_parse_author + 1
        # possible values are 1--> Valid entry, 2--> Invalid entry and 3 --> Unknown entry
        found = 0
        author_link = ''
        # date of birth
        dob = ''
        # date of death
        dod = ''

        author_link = response.url
        
        print "Parsing author No. ", self.count_parse_author
	
        try:
            dob = response.xpath("//div[@id='mw-content-text']/table[@id='kkparichay-box']//div[@id='kkparichay-dob']/text()").extract()[0]	
            #print dob
            self.count_dob = self.count_dob + 1
        except:
            pass
        
        try:
            dod = response.xpath("//div[@id='mw-content-text']/table[@id='kkparichay-box']//div[@id='kkparichay-dod']/text()").extract()[0]	
            #print dod
            self.count_dod = self.count_dod + 1
        except:
            pass
        
        if dod:
           
            try:
                year = dod.split()[-1]
                year = int(year)
                if year > datetime.now().year - 60:
                    #print "Author is not valid for further processing: dod < 60 "
                    found = 2
                else:
                    self.count_valid = self.count_valid +1
                    found = 1
            except:
                #print "ERROR:: DOD: ", dod
                self.count_invalid_yr = self.count_invalid_yr + 1
                found = 3
        elif dob:
            
            try:
                year = dob.split()[-1]
                year = int(year)
                if year > datetime.now().year - 120:
                    #print "Author is not valid for furthur processing: dob < 120"
                    found = 2
                else:
                    self.count_valid = self.count_valid +1
                    found = 1
            except:
                #print "ERROR:: DOB: ", dob
                self.count_invalid_yr = self.count_invalid_yr + 1
                found = 3
        else:
            #print "Author is not valid for further processing: dod and dob not found"
            self.count_invalid_yr = self.count_invalid_yr + 1
            found = 3
            
        if found == 1:
            """
            Parse the page, find out the articles list, generate request for each article
            Extract article links from the Author page and generate request for each
            """
            try:
                print "Extracting poem links from Author page"
                articles = response.xpath("//div[@id='mw-content-text']/ul/li/a/@href").extract()
        
                articles_links = [self.domain_name+x for x in articles]
                for url in articles_links:
                    print "Visiting Article: ", url
                    yield scrapy.Request(url, callback=self.parse_article_page)
            except:
                print "Nothing found in Author page!!!"
            
        elif found == 2:
            with open("KK_invalid_author.txt", "a") as outfile:
                json.dump({'link': author_link, 'dob':dob, 'dod':dod}, outfile, indent=4)
        elif found == 3:
            with open("KK_unknown_author.txt", "a") as outfile:
                json.dump({'link': author_link, 'dob':dob, 'dod':dod}, outfile, indent=4)

                    
        """
        print "-----------------------------------------"
        print "Parsed: ", self.count_parse_author
        print "Valid:  ", self.count_valid
        print "Short URL:  ", self.count_surl
        print "DoB: ", self.count_dob, "DoD: ", self.count_dod
        print "Invalid Year: ", self.count_invalid_yr
        print "-----------------------------------------"
        """
        
        #yield { 'link': author_link, 'dob':dob, 'dod':dod }
    

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
            """
            Extract article links from the Author page and generate request for each
            """
            try:
                print "Extracting poem links from Author page"
                articles = response.xpath("//div[@id='mw-content-text']/ul/li/a/@href").extract()
        
                articles_links = [self.domain_name+x for x in articles]
                for url in articles_links:
                    print "Visiting Article: ", url
                    yield scrapy.Request(url, callback=self.parse_article_page)
            except:
                print "Nothing found in Author page!!!"
            
