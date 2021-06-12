'''
Post processing of data crawled by ``KangarooBot`` of kavitakosh.org
'''
from exceptions import Exception
from threading import Thread
from django.shortcuts import render, get_object_or_404

from crawlers.models import RawArticle


def refine_title(article_title):
    '''
    kavitakosh titles are like..
    'title / poet' or 'title / book or section / poet'
    Here, we will remove the last part, 'poet'.
    '''
    try:
        ts = article_title.split('/')[:-1]
        if ts:    
            t = '/'.join(ts)
        else:
            t = None
    except Exception as e:
        print('ERR:: Exception occurred.')
        print(e)
        return None
        
    return t


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


def process_articles(name=None, articles=None):
    '''
    Process given list of articles.
    '''
    count_total = 0
    count_saved = 0
        
    if articles is not None:
        for obj in articles:
            count_total += 1
            t = refine_title(obj.title)
            if t:
                obj.title = t
                obj.save()
                count_saved += 1

            # print stats
            if count_total % 100 == 0:
                print("> thread %s: saved %d out of %d processed"%(name, count_saved, count_total))    
    
    
def process_all_articles(num_thread=1):
    '''
    @summary: Post processing of all articles crawled by the ``KangarooBot``
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


def cmd_init_kangaroo():
    print('============= Initializing reindeer ==============')
    print('================ init finished ===================')

def cmd_resume_kangaroo(num_thread=1):
    print('=========== Resuming/running reindeer ============')
    process_all_articles(num_thread)
    print('=============== resume finished ==================')

def cmd_exit_kangaroo():
    print('============= Exiting reindeer ==============')
    print('================ exit finished ===================')
    
def cmd_test_kangaroo():
    print('=============== Testing reindeer =================')
    obj = get_object_or_404(RawArticle, pk=167888)
    print(obj.title)
    title = refine_title(obj.title)
    print('================= test finished ==================')
    print(title)