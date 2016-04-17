from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse

#from django_libs.utils_email import send_email

from feedback.models import Feedback


class FeedbackForm(forms.ModelForm):
    '''
    A feedback form with modern spam protection.
    :url: Field to trap spam bots.
    '''
    
    url = forms.URLField(required=False)

    def __init__(self, user=None, url=None, prefix='feedback',
                 content_object=None, *args, **kwargs):
        print "DBG:: FeedbackForm  init."
        self.content_object = content_object
        super(FeedbackForm, self).__init__(prefix='feedback', *args, **kwargs)
        if url:
            self.instance.url = url
        if user:
            self.instance.added_by = user
            del self.fields['email']
        else:
            self.fields['email'].required = True

    def save(self):
        print "DBG:: FeedbackForm  save."
        if not self.cleaned_data.get('url'):
            self.instance.content_object = self.content_object
            obj = super(FeedbackForm, self).save()
            print "DBG:: FeedbackForm saved", obj.id
#             send_email(
#                 '',
#                 {
#                     'url': reverse('admin:feedback_form_feedback_change',
#                                    args=(obj.id, )),
#                     'feedback': obj,
#                 },
#                 'feedback_form/email/subject.html',
#                 'feedback_form/email/body.html',
#                 from_email=settings.FROM_EMAIL,
#                 recipients=[manager[1] for manager in settings.MANAGERS],
#             )
#             if getattr(settings, 'FEEDBACK_EMAIL_CONFIRMATION', False):
#                 email = None
#                 if obj.email:
#                     email = obj.email
#                 elif obj.user.email:
#                     email = obj.user.email
#                 if email:
#                     send_email(
#                         '', {},
#                         'feedback_form/email/confirmation_subject.html',
#                         'feedback_form/email/confirmation_body.html',
#                         from_email=settings.FROM_EMAIL,
#                         recipients=[email],
#                     )
            return obj

    class Media:
        css = {'all': ('feedback/css/feedback.css'), }
        js = ('feedback/js/feedback.js', )

    class Meta:
        model = Feedback
        fields = ('email', 'text')