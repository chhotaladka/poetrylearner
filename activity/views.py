from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from activity.models import Action


@login_required
def activity_list(request):
    '''
    @summary: List all the activities by the user
    '''
    obj_list = Action.objects.all()
    
    # Pagination
    paginator = Paginator(obj_list, 40) # Show 40 entries per page    
    page = request.GET.get('page')
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objs = paginator.page(paginator.num_pages)

    context = {'actions': objs,}
    template = 'activity/list.html'

    return render(request, template, context)