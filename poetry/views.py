from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request
from django.contrib import messages
import os, sys, traceback
import json
from django.contrib.sites.shortcuts import get_current_site
from meta_tags.views import Meta
from repository.views import readers

# Create your views here. 


def welcome(request):
    '''
    Welcome page
    ''' 
    poetry = readers.get_a_poetry()
    
    # Instantiate the Meta class
    meta_image_url = "img/poetrylearner_logo_120x120.png"
    meta_description = "Building towards an archive for the poetry of every language. Read your next favorite poetry."
    
    meta = Meta(title = "Read a random Poetry on %s"%(get_current_site(request).name), 
                description = meta_description,
                keywords = None,
                image = meta_image_url,
            )
    
    context = {'poetry': poetry, 'meta': meta,}
    template = 'welcome.html'
    
    return render(request, template, context)


def book(request, pk, slug):
    '''
    Returns the book from the repository
    '''    
    return readers.item(request, 'book', pk, slug, src='public_url')


def poet(request, pk, slug):
    '''
    Returns the person from the repository
    '''    
    return readers.item(request, 'person', pk, slug, src='public_url')


def poetry(request, pk, slug):
    '''
    Returns the poetry from the repository
    '''    
    return readers.item(request, 'poetry', pk, slug, src='public_url')


def explore_books_of(request, pk, slug):
    '''
    @summary: Returns the books by the person `pk` from the repository
    '''
    return readers.explore_books(request, poet=pk, slug=slug, src='public_url')


def explore_poetry_of(request, pk, slug):
    '''
    @summary: Returns the poetry by the person `pk` from the repository
    '''
    return readers.explore_poetry(request, poet=pk, slug=slug, src='public_url')


def explore_books(request):
    '''
    Returns the list of books from the repository
    '''
    return readers.explore_books(request, src='public_url')


def explore_poets(request):
    '''
    Returns the list of persons from the repository
    '''    
    return readers.explore_poets(request, src='public_url')


def explore_poetry(request):
    '''
    Returns the list of poetries from the repository
    '''
    return readers.explore_poetry(request, src='public_url')


def explore_tags(request, slug):
    '''
    Returns the list of tagged items from the repository
    '''    
    return readers.explore_tags(request, slug, src='public_url')