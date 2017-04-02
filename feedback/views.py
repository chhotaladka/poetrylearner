from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone

from common.decorators import group_required
from common.utils import user_has_group
from feedback.forms import FeedbackForm
from feedback.models import Feedback, FEEDBACK_RATING_MAX, FEEDBACK_RATING_MIN

# Create your views here.

class FeedbackCreateView(CreateView):
    '''
    View to display and handle a feedback create form.
    '''
    
    model = Feedback
    form_class = FeedbackForm
    #template_name = 'feedback/feedback_form.html'
    ajax_template = 'feedback/form.html'
    thanks_template = 'feedback/include/thanks.html'
    error_template = 'feedback/include/error.html'

    def dispatch(self, request, *args, **kwargs):
        #print "FeedbackCreateView dispatch."
        if kwargs.get('ctype_id') and kwargs.get('obj_id'):
            try:
                content_type = ContentType.objects.get_for_id(kwargs['ctype_id'])
            
            except ContentType.DoesNotExist:
                if request.is_ajax():
                    # Create JSON response and send
                    data = {}
                    data['status'] = '404'
                    data['contenthtml'] = render_to_string(
                                            self.error_template,
                                            context={'error_message': 'invalid content'}
                                        )
                    return JsonResponse(data)
                raise Http404
            
            try:
                self.content_object = content_type.get_object_for_this_type(pk=kwargs['obj_id'])
                self.ctype_id = kwargs['ctype_id']

            except ObjectDoesNotExist:
                if request.is_ajax():
                    # Create JSON response and send
                    data = {}
                    data['status'] = '404'
                    data['contenthtml'] = render_to_string(
                                            self.error_template,
                                            context={'error_message': 'invalid object'}
                                        )
                    return JsonResponse(data)
                raise Http404
            
        return super(FeedbackCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        #print "FeedbackCreateView get_form_kwargss."
        kwargs = super(FeedbackCreateView, self).get_form_kwargs()
        
        if self.request.user.is_authenticated():
            kwargs.update({'user': self.request.user})
        
        kwargs.update({
            'url': self.request.META.get('HTTP_REFERER', self.request.path),
            'content_object': self.content_object if hasattr(self, 'content_object') else None,
        })
        return kwargs

    def get_template_names(self):
        #print "FeedbackCreateView get_template_names."
        if self.request.is_ajax():
            return self.ajax_template
        
        return super(FeedbackCreateView, self).get_template_names()

    def get_context_data(self, **kwargs):
        #print "FeedbackCreateView get_context_data."
        context = super(FeedbackCreateView, self).get_context_data(**kwargs)
        
        if hasattr(self, 'content_object'):
            context.update({'content_object': self.content_object})

        if hasattr(self, 'ctype_id'):
            context.update({'ctype_id': self.ctype_id})
            
        return context

    def post(self, request, *args, **kwargs):
        '''
        Check for spam
        '''
        xx = request.POST.get('xx', None)
        yy = request.POST.get('yy', None)
        if xx or yy:
            print "WARN:: spam detected."
            if request.is_ajax():
                # Create JSON response and send
                data = {}
                data['status'] = '400'
                data['contenthtml'] = render_to_string(
                                        self.error_template,
                                        context={'error_message': 'invalid access'}
                                    )
                return JsonResponse(data)
            raise Http404
        
        return super(FeedbackCreateView, self).post(request, *args, **kwargs)
    
    def form_valid(self, form):
        """
        If the form is valid-
            1. save the associated model
            2. redirect to the supplied URL.
        """
        self.object = form.save()
        
        if self.request.is_ajax():
            # Create JSON response and send
            data = {}
            data['status'] = '200'
            data['contenthtml'] = render_to_string(self.thanks_template)
            return JsonResponse(data)
        return HttpResponseRedirect(self.get_success_url())
   
    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        if self.request.is_ajax():
            # Create JSON response and send
            data = {}
            data['status'] = '422' # Unprocessable Entity
            data['contenthtml'] = render_to_string(
                                    self.error_template,
                                    context={'error_message': 'invalid data'}
                                )
            return JsonResponse(data)
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return '/'
   

@group_required('administrator')
def feedback_response(request, pk):
    '''
    @summary: View details of a feedback and give response if action has been taken.
    '''
    obj = get_object_or_404(Feedback, pk=pk)    

    if request.method == "POST":
        action = request.POST.get('action', None)
        notify = request.POST.get('notify', None)
        rating = request.POST.get('rating', None)
        
        # validate data and process
        flag_save = False
        
        if rating:
            try:
                rating = int(rating)
                if FEEDBACK_RATING_MIN <= rating <= FEEDBACK_RATING_MAX:
                    obj.rating = rating
                    flag_save = True
            except ValueError:
                    pass  # it was not an int.
        
        if action != None and action != '':
            if len(action) < 1000:
                obj.action = action
                flag_save = True
            else:
                flag_save = False
                message = 'Failed. Maximum allowed response length is 1000 characters.'
        else:
            flag_save = False
            message = 'Failed. Response should not be empty.' 

        if flag_save:
            obj.date_responded = timezone.now()
            obj.save()
            message = 'Response submitted successfully!'
            
            # Check notify
            if notify:
                user_email = obj.get_user_email()
                if user_email:
                    # Send email to the user
                    print 'DBG:: in response to feedback %s, sending email to %s'% (obj.id, user_email)
                    message += ' Notification sent to user.'
            
        messages.success(request, message)
        return HttpResponseRedirect(obj.get_absolute_url())

    ##
    # Make the context and render            
    context = {'feedback': obj}
    template = "feedback/response.html"

    return render(request, template, context)


def _create_query_list(request, q=None, extra_get_queries=[]):
    '''
    @summary: Return query list object for feedbacks
    '''
    get_query = ''.join(extra_get_queries)
    url = request.path
    
    q_name = {
              'all': 'All',
              'pending': 'Pending',
              'closed': 'Closed',
              'me': 'My feedbacks',
              'anonymous': 'Anonymous',
              'known': 'By known'
            }
    
    # Create query list and populate
    query_list = []
    
    item = {
           'name': q_name['all'],
           'help_text': 'Recent feedbacks',
           'url': url + '?q=all',
           'css': 'is-active' if q == 'all' else '',
        }
    query_list.append(item)
    
    item = {
           'name': q_name['pending'],
           'help_text': 'Feedbacks to which response is awaiting.',
           'url': url + '?q=pending',
           'css': 'is-active' if q == 'pending' else '',
        }
    query_list.append(item)
    
    item = {
           'name': q_name['closed'],
           'help_text': 'Feedbacks to which response has given.',
           'url': url + '?q=closed',
           'css': 'is-active' if q == 'closed' else '',
        }
    query_list.append(item)
    
    item = {
           'name': q_name['me'],
           'help_text': 'My feedbacks',
           'url': url + '?q=me',
           'css': 'is-active' if q == 'me' else '',
        }
    query_list.append(item)
    
    if user_has_group(request.user, ['Administrator',]):
        item = {
               'name': q_name['anonymous'],
               'help_text': 'Feedbacks by anonymous users',
               'url': url + '?q=anonymous',
               'css': 'is-active' if q == 'anonymous' else '',
            }
        query_list.append(item)
        
        item = {
               'name': q_name['known'],
               'help_text': 'User has account or have given email id',
               'url': url + '?q=known',
               'css': 'is-active' if q == 'known' else '',
            }
        query_list.append(item)
    
    return query_list, q_name[q]


@group_required('administrator', 'editor')
def feedback_list(request):
    '''
    @summary: List all the feedbacks submitted till now by users
    '''
        
    q_objects = Q()
    obj_list = []
    
    ##
    # Check the parameters passed in the URL and process accordingly
    
    # Query tab
    q_tab = request.GET.get('q', None)
    
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
                                                  ).order_by('-date_responded')
            
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
    elif q_tab == 'me':
        # Feedbacks by me i.e. request.user        
        obj_list = Feedback.objects.all().filter(
                                                 Q(added_by=request.user)
                                                 )
    elif q_tab == 'all':
        # Most recent feedbacks
        obj_list = Feedback.objects.all()
 
    else:
        # Default: Feedbacks to which we have not responded
        q_tab = 'pending'
        obj_list = Feedback.objects.all().filter(
                                                  Q(action__isnull=True) |
                                                  Q(action=u'')
                                                  )

    # Create query list and its title
    query_list, query_list_title = _create_query_list(request, q_tab)
    
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
        
    context = {'feedbacks': objs,
               'query_list': query_list,
               'query_list_title': query_list_title
               }
    template = 'feedback/list.html'

    return render(request, template, context)