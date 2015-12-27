from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.context_processors import request
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
import os, sys, traceback
import json

# Create your views here.


def home(request):
    result = 'Ghar aa gaye!!'
    r = json.dumps(result)
                  
    return HttpResponse(r, content_type="application/json") 