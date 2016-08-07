from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from activity.models import Action


@login_required
def activity_list(request):
    '''
    @summary: List all the activities by the user
    '''
    obj_list = Action.objects.all()
    
    objs = obj_list

    context = {'actions': objs,}
    template = 'activity/list.html'

    return render(request, template, context)