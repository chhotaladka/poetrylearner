from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def activity_list(request):
    '''
    @summary: List all the activities by the user
    '''
    objs = None

    context = {'activities': objs,}
    template = 'activity/list.html'

    return render(request, template, context)