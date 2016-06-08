from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request
from django.contrib import messages
import os, sys, traceback
import json

from repository.views import readers

# Create your views here. 


def welcome(request):
    '''
    Welcome page
    ''' 
    poetry = readers.get_a_poetry()

    context = {'poetry': poetry}
    template = 'welcome.html'
    
    return render(request, template, context)


def poetry(request, pk, slug):
    '''
    Returns the poetry from the repository
    '''    
    return readers.item(request, 'poetry', pk, slug)


def poet(request, pk, slug):
    '''
    Returns the person from the repository
    '''    
    return readers.item(request, 'person', pk, slug)


def list_poetry(request):
    '''
    Returns the list of poetries from the repository
    '''    
    return readers.list(request, 'poetry')


def list_poet(request):
    '''
    Returns the list of persons from the repository
    '''    
    return readers.list(request, 'person')