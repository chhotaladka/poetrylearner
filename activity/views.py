from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Max
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth.models import User
from activity.models import Action, VERBS

def _create_query_tabs(request_path='/', q_tab=None, extra_get_queries=[]):
    '''
    @summary: Return query tab object for Activity
    '''
    get_query = ''.join(extra_get_queries)
    
    # Create tab list and populate
    query_tabs = []
    
    tab = {
           'name': 'My Logs',
           'help_text': 'My Activity Logs',
           'url': reverse('activity:list') + '?' + get_query,
           'css': 'is-active' if q_tab == 'mylogs' or q_tab is None else '',
        }
    query_tabs.append(tab)
    
    tab = {
           'name': 'Everything',
           'help_text': 'See what others are doing',
           'url': reverse('activity:list-all') + '?' + get_query,
           'css': 'is-active' if q_tab == 'everything' else '',
        }
    query_tabs.append(tab)
    
    return query_tabs


def _create_query_list(request_path='/', period=None, extra_get_queries=[]):
    '''
    @summary: Return query list object for Contributors
    '''
    get_query = ''.join(extra_get_queries)
    
    # Create tab list and populate
    query_list = []
    
    tab = {
           'name': 'All time',
           'help_text': 'Top contributors of all time',
           'url': reverse('activity:contributors') + '?p=alltime' + get_query,
           'css': 'is-active' if period == 'alltime' or period is None else '',
        }
    query_list.append(tab)
    
    tab = {
           'name': 'Fortnightly',
           'help_text': 'Top contributors of the last fortnight',
           'url': reverse('activity:contributors') + '?p=fortnight' + get_query,
           'css': 'is-active' if period == 'fortnight' else '',
        }
    query_list.append(tab)
    
    tab = {
           'name': 'Monthly',
           'help_text': 'Top contributors of the last month',
           'url': reverse('activity:contributors') + '?p=month' + get_query,
           'css': 'is-active' if period == 'month' else '',
        }
    query_list.append(tab)
    
    tab = {
           'name': 'Yearly',
           'help_text': 'Top contributors of the last year',
           'url': reverse('activity:contributors') + '?p=year' + get_query,
           'css': 'is-active' if period == 'year' else '',
        }
    query_list.append(tab)
    
    return query_list


def __activity_list(request, show_all=False):
    '''
    @summary: Activities list
    '''
    
    query_tabs = []
    extra_get_queries = []
    stats = []
    
    if show_all:
        q_tab = 'everything'
        obj_list = Action.objects.all()
    else:
        q_tab = 'mylogs'
        obj_list = Action.objects.actor(request.user)
    
    # Create statistics
    data = {}
    data['name'] = 'unpublished'
    data['value'] = obj_list.filter(verb=VERBS['UNPUBLISH']).count()
    stats.append(data)
    
    data = {}
    data['name'] = 'published'
    data['value'] = obj_list.filter(verb=VERBS['PUBLISH']).count()
    stats.append(data)
    
    data = {}
    data['name'] = 'updated'
    data['value'] = obj_list.filter(verb=VERBS['CHANGE']).count()
    stats.append(data)
    
    data = {}
    data['name'] = 'added'
    data['value'] = obj_list.filter(verb=VERBS['ADDITION']).count()
    stats.append(data)
    
    query_tabs = _create_query_tabs(request.path, q_tab, extra_get_queries)
    
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

    context = {'actions': objs,
               'query_tabs': query_tabs,
               'stats': stats,}
    template = 'activity/list.html'

    return render(request, template, context)


@login_required
def activity_list(request):
    '''
    @summary: List all the activities by the user
    '''
    return __activity_list(request, show_all=False)


@login_required
def activity_list_all(request):
    '''
    @summary: List all the activities
    '''
    return __activity_list(request, show_all=True)


@login_required
def list_contributors(request):
    '''
    @summary: List contributors(users/actors) having activities recently (in last fortnight).
    Short in decereasing order of number of activities.
    '''
    RESULT_COUNT = 5
    
    # Check the parameters passed in the URL and process accordingly
    period = request.GET.get('p', None)
    
    if period == 'fortnight':
        num_days = 15
    elif period == 'month':
        num_days = 30
    elif period == 'year':
        num_days = 365
    else:
        # Collect all time data
        num_days = 0
        period = None
    
    # Generate queryset
    if num_days:
        qset = User.objects.filter(
                                   action__timestamp__gte = timezone.now().date() - timedelta(days=num_days)
                                   )
    else:
       qset = User.objects.all()
       
    objs = qset.annotate(
                         num_actions=Count('action'),
                         lastest_action_date=Max('action__timestamp')
                         ).order_by('-num_actions')[:RESULT_COUNT]
    
    #
    query_list = _create_query_list(request.path, period)
    
    
    context = {'contributors': objs,
               'query_list': query_list,
               }
    template = 'activity/contributors.html'

    return render(request, template, context)
