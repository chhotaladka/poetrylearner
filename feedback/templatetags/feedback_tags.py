from django import template
from feedback.forms import FeedbackForm

FEEDBACK_FORM_COLOR =  '#6caec9'
FEEDBACK_FORM_TEXTCOLOR = '#fff'
FEEDBACK_FORM_TEXT = ''

register = template.Library()


@register.inclusion_tag('feedback/form.html', takes_context=True)
def feedback_form(context):
    """Template tag to render a feedback form."""
    print("DBG:: feedback_tags.")
    user = None
    url = None
    if context.get('request'):
        url = context['request'].path
        if context['request'].user.is_authenticated():
            user = context['request'].user
    return {
        'form': FeedbackForm(url=url, user=user),
        'background_color': FEEDBACK_FORM_COLOR,
        'text_color': FEEDBACK_FORM_TEXTCOLOR,
        'text': FEEDBACK_FORM_TEXT,
    }