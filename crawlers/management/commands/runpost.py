from django.core.management.base import BaseCommand, CommandError
import sys
import traceback

from crawlers.processors.reindeer import cmd_init_reindeer, cmd_resume_reindeer, cmd_exit_reindeer
from crawlers.processors.kangaroo import cmd_init_kangaroo, cmd_resume_kangaroo, cmd_exit_kangaroo

class Command(BaseCommand):
    help = 'Run crawlers post processing commands.'

    def add_arguments(self, parser):
        # Positional arguments
      
        # Named (optional) arguments
        parser.add_argument(
            '--init',
            type=str,
            choices=['reindeer', 'kangaroo'],
            dest='init',
            default=False,
            help='Initialize post processor.',
        )
        parser.add_argument(
            '--resume',
            type=str,
            choices=['reindeer', 'kangaroo'],
            dest='resume',
            default=False,
            help='Resume/run post processor.',
        )
        parser.add_argument(
            '--exit',
            type=str,
            choices=['reindeer', 'kangaroo'],
            dest='exit',
            default=False,
            help='Exit post processor.',
        )
        parser.add_argument(
            '-t',
            '--thread',
            type=int,
            dest='thread',
            default=False,
            help='Number of threads to be created for processing.',
        )                                

    def handle(self, *args, **options):
        
        if options['thread'] > 1:
            num_thread = options['thread']
        else:
            num_thread = 1
                
        if options['init']:
            process = options['init']
            if process == 'reindeer':
                cmd_init_reindeer()
                
            elif process == 'kangaroo':
                cmd_init_kangaroo()
                
        elif options['resume']:
            process = options['resume']
            if process == 'reindeer':
                cmd_resume_reindeer(num_thread)
                
            elif process == 'kangaroo':
                cmd_resume_kangaroo(num_thread)
                
        elif options['exit']:
            process = options['exit']
            if process == 'reindeer':
                cmd_exit_reindeer()
                
            elif process == 'kangaroo':
                cmd_exit_kangaroo()
        else:
            raise CommandError('-h or --help for help')       