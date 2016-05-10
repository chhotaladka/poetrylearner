from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
import os, sys, traceback

from bookmarks.models import Bookmark 

# Create your views here.

@login_required
def create_bookmark(request):
    '''
    '''
    pass


@login_required
def delete_bookmark(request):
    '''
    '''
    pass