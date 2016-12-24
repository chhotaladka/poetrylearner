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
    return readers.item(request, 'poetry', pk, slug, src='public_url')


def poet(request, pk, slug):
    '''
    Returns the person from the repository
    '''    
    return readers.item(request, 'person', pk, slug, src='public_url')


def explore_poetry_of(request, pk, slug):
    '''
    @summary: Returns the poetry by the person `pk` from the repository
    '''
    return readers.explore_poetry(request, poet=pk, slug=slug, src='public_url')


def explore_poetry(request):
    '''
    Returns the list of poetries from the repository
    '''
    return readers.explore_poetry(request, src='public_url')


def explore_poets(request):
    '''
    Returns the list of persons from the repository
    '''    
    return readers.explore_poets(request, src='public_url')


def explore_tags(request, slug):
    '''
    Returns the list of tagged items from the repository
    '''    
    return readers.explore_tags(request, slug, src='public_url')