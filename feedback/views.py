from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.validators import validate_email

from common.decorators import group_required
from feedback.forms import FeedbackForm
from feedback.models import Feedback

# Create your views here.

class FeedbackCreateView(CreateView):
    '''
    View to display and handle a feedback create form.
    '''
    
    model = Feedback
    form_class = FeedbackForm
    #template_name = 'feedback/feedback_form.html'
    ajax_template = 'feedback/form_content.html'

    def dispatch(self, request, *args, **kwargs):
        print "FeedbackCreateView dispatch."
        if kwargs.get('ctype_id') and kwargs.get('obj_id'):
            try:
                content_type = ContentType.objects.get_for_id(kwargs['ctype_id'])
                print content_type
            except ContentType.DoesNotExist:
                raise Http404
            
            try:
                self.content_object = content_type.get_object_for_this_type(pk=kwargs['obj_id'])
                self.ctype_id = kwargs['ctype_id']                

            except ObjectDoesNotExist:
                raise Http404
            
        return super(FeedbackCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        print "FeedbackCreateView get_form_kwargss."
        kwargs = super(FeedbackCreateView, self).get_form_kwargs()
        
        if self.request.user.is_authenticated():
            kwargs.update({'user': self.request.user})
        
        kwargs.update({
            'url': self.request.META.get('HTTP_REFERER', self.request.path),
            'content_object': self.content_object if hasattr(self, 'content_object') else None,
        })
        return kwargs

    def get_template_names(self):
        print "FeedbackCreateView get_template_names."
        if self.request.is_ajax():
            return self.ajax_template
        
        return super(FeedbackCreateView, self).get_template_names()

    def get_context_data(self, **kwargs):
        print "FeedbackCreateView get_context_data."
        context = super(FeedbackCreateView, self).get_context_data(**kwargs)
        
        if hasattr(self, 'content_object'):
            context.update({'content_object': self.content_object})

        if hasattr(self, 'ctype_id'):
            context.update({'ctype_id': self.ctype_id})                       
            
        return context

    def get_success_url(self):
        return reverse('feedback:add')
   

@group_required('administrator')
def feedback_response(request, pk):
    '''
    @summary: View details of a feedback and give response if action has been taken.
    '''
    obj = get_object_or_404(Feedback, pk=pk)    

    if request.method == "POST":
        action = request.POST.get('action')
        notify = request.POST.get('notify')
        print action
        
        # validate and clean data
#         if action == 'Publish':
#             obj.date_published = timezone.now()
#         elif action == 'Unpublish':
#             obj.date_published = None
#         obj.save()

        print notify
        if notify:
            user_email = obj.get_user_email()
            if user_email:               
                # Send email to the user
                print 'DBG:: in response to feedback %s, sending email to %s'% (obj.id, user_email)
                pass

        messages.success(request, 'Response submitted successfully!')
        return HttpResponseRedirect(obj.get_absolute_url())

    ##
    # Make the context and render            
    context = {'feedback': obj}
    template = "feedback/response.html"

    return render(request, template, context)    


@group_required('administrator')
def feedback_list(request):
    '''
    @summary: List all the feedbacks submitted till now by users
    '''
        
    q_objects = Q()
    obj_list = []
    
    ##
    # Check the parameters passed in the URL and process accordingly
    
    # Query tab
    q_tab = request.GET.get('tab', None)
    
    if q_tab == 'pending':
        # Feedbacks to which we have not responded
        obj_list = Feedback.objects.all().filter(
                                                  Q(action__isnull=True) | 
                                                  Q(action=u'')
                                                  )

    elif q_tab == 'closed':
        # Feedbacks to which we have responded
        obj_list = Feedback.objects.all().exclude(
                                                  Q(action__isnull=True) | 
                                                  Q(action=u'')
                                                  )
            
    elif q_tab == 'known':
        # User has account or have given email id
        obj_list = Feedback.objects.all().filter(
                                                 Q(added_by__isnull=False) |
                                                 Q(email__isnull=False)
                                                 ).exclude(email=u'')
        
    elif q_tab == 'anonymous':
        # Feedbacks by anonymous users (haven't given email id)        
        obj_list = Feedback.objects.all().filter(
                                                 Q(added_by__isnull=True),
                                                 Q(email__isnull=True) | 
                                                 Q(email=u'')
                                                 )        
    
    elif q_tab == 'all':
        # Most recent feedbacks
        obj_list = Feedback.objects.all()
 
    else:
        # Default: Most recent feedbacks
        obj_list = Feedback.objects.all()
          
    
    # Create tab list and populate
    query_tabs = []    
    
    tab = {
           'name': 'all',
           'help_text': 'Recent feedbacks',
           'url': request.path + '?tab=all',
           'css': 'is-active' if q_tab == 'all' or q_tab is None else '',
        }
    query_tabs.append(tab)
    
    tab = {
           'name': 'pending',
           'help_text': 'Feedbacks to which we have not responded',
           'url': request.path + '?tab=pending',
           'css': 'is-active' if q_tab == 'pending' else '',
        }
    query_tabs.append(tab)
    
    tab = {
           'name': 'closed',
           'help_text': 'Feedbacks to which we have responded',
           'url': request.path + '?tab=closed',
           'css': 'is-active' if q_tab == 'closed' else '',
        }
    query_tabs.append(tab)
    
    tab = {
           'name': 'by anonymous',
           'help_text': 'Feedbacks by anonymous users',
           'url': request.path + '?tab=anonymous',
           'css': 'is-active' if q_tab == 'anonymous' else '',
        }
    query_tabs.append(tab)
    
    tab = {
           'name': 'by known',
           'help_text': 'User has account or have given email id',
           'url': request.path + '?tab=known',
           'css': 'is-active' if q_tab == 'known' else '',
        }
    query_tabs.append(tab)
            
    
    # Pagination
    paginator = Paginator(obj_list, 20) # Show 20 entries per page    
    page = request.GET.get('page')
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objs = paginator.page(paginator.num_pages)
            
    context = {'feedbacks': objs, 'query_tabs': query_tabs}
    template = 'feedback/list.html'    

    return render(request, template, context)    