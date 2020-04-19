'''
Delete the RawArticle having empty/missing/partial `content`
'''
from exceptions import Exception
from threading import Thread
from django.shortcuts import render, get_object_or_404

from crawlers.models import RawArticle
from crawlers.utils import ARTICLE_MIN_LEN
from django.utils.html import strip_tags


def is_content_invalid(content):
    '''
    Returns True if `obj.content` is empty/missing or it's size is smaller than expected.
    # Here we assume that the length of content should be greater than `ARTICLE_MIN_LEN`. 
    '''
    try:
        c = strip_tags(content)
        if len(c) <= ARTICLE_MIN_LEN:
            return True
        
    except Exception as e:
        print('ERR:: Exception occurred.')
        print(e)
        
    return False


def process_articles(name=None, articles=None):
    '''
    Process given list of articles.
    '''
    count_total = 0
    count_action = 0
        
    if articles is not None:
        for obj in articles:
            count_total += 1
            if is_content_invalid(obj.content):
                # Delete the entry
                print("Deleting article %s..." % obj.id)
                obj.delete()
                count_action += 1

            # print stats
            if count_total % 100 == 0:
                print("> thread %s: action taken %d out of %d processed"%(name, count_action, count_total))    


class processArticleThread(Thread):
    '''
    @summary: process articles in multithreads
    '''    
    def __init__(self, threadID, name, articles):
        Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.articles = articles
        
    def run(self):
        print(">> Starting thread " + self.name)
        process_articles(self.name, self.articles)
        print(">> Ending thread " + self.name)


def process_all_articles(num_thread=1):
    '''
    @summary: Post processing of all crawled articles
    '''
    if num_thread < 1:
        num_thread = 1

    total_articles = RawArticle.objects.all().filter(source_url__icontains='kavitakosh.org')
    num_total = total_articles.count()
    print('Total articles to be proccessed : %d'%(num_total))
    print('Number of threads to be created : %d'%(num_thread))
    q = num_total / num_thread
    r = num_total - (q * num_thread)
        
    threads = []
    
    # Create new threads
    for i in range(0, num_thread):
        extra = r if (i == (num_thread - 1)) else 0
        num_start = i*q
        num_end = num_start + q + extra
        thread_name = 'Thread-'+str(i)
        
        print('Starting thread for total_articles[%d : %d]'%(num_start, num_end))
        
        t = processArticleThread(i, thread_name, total_articles[num_start : num_end])
        t.start()
        threads.append(t)
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    print("Exiting Main Thread")

    # print stats
    print("> THE END")


def cmd_init_cleaning():
    print('============= Initializing cleaning ==============')
    print('================ init finished ===================')

def cmd_resume_cleaning(num_thread=1):
    print('=========== Resuming/running cleaning ============')
    process_all_articles(num_thread)
    print('=============== resume finished ==================')

def cmd_exit_cleaning():
    print('============= Exiting cleaning ==============')
    print('================ exit finished ===================')
    
def cmd_test_cleaning():
    print('=============== Testing cleaning =================')
    obj = get_object_or_404(RawArticle, pk=167888)
    print(obj.content)
    if is_content_invalid(obj.content):
        print("Content is invaild.")
    else:
        print("Content is valid.")
    print('================= test finished ==================')