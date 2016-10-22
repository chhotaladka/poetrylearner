from django.core.management.base import BaseCommand, CommandError
import sys
import traceback

from crawlers.spiders import *

class Command(BaseCommand):
    help = 'Run crawler commands.'

    def add_arguments(self, parser):
        # Positional arguments
      
        # Named (optional) arguments
        parser.add_argument(
            '--test',
            type=str,
            choices=['reindeer', 'kangaroo'],
            dest='test',
            default=False,
            help='Run tests to verify the working of spider.',
        )
        parser.add_argument(
            '--resume',
            type=str,
            choices=['reindeer', 'kangaroo'],
            dest='resume',
            default=False,
            help='Resume/run selected spider.',
        )

    def handle(self, *args, **options):
        
        if options['test']:
            process = options['test']
            if process == 'reindeer':
                obj = SpiderReindeer()
                obj.test()
                
            elif process == 'kangaroo':
                obj = SpiderKangaroo()
                obj.test()
            
        elif options['resume']:
            process = options['resume']
            if process == 'reindeer':
                obj = SpiderReindeer()
                obj.resume()
                
            elif process == 'kangaroo':
                obj = SpiderKangaroo()
                obj.resume()
            
        else:
            raise CommandError('-h or --help for help')