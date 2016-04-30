from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request
from django.contrib import messages
import os, sys, traceback
import json

from repository.views.readers import get_a_poetry

# Create your views here. 


def welcome(request):
    
    ##
    # Make the context and render 
    poetry = get_a_poetry()

    context = {'poetry': poetry}
    template = 'welcome.html'
    
    return render(request, template, context) 