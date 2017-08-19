#
# All constants could be used in other modules
#


# This is defined here as a do-nothing function because we can't import
# django.utils.translation -- that module depends on the settings.
gettext_noop = lambda s: s

# Supported Languages for the contents of the Repository
# It is derived from django.conf.global_settings.LANGUAGES
REPOSITORY_LANGUAGES = [
    ('bn', gettext_noop('Bengali')),
    ('en', gettext_noop('English')),
    ('hi', gettext_noop('Hindi')),
    ('kn', gettext_noop('Kannada')),
    ('ml', gettext_noop('Malayalam')),
    ('mr', gettext_noop('Marathi')),
    ('ne', gettext_noop('Nepali')),
    ('pa', gettext_noop('Punjabi')),
    ('ta', gettext_noop('Tamil')),
    ('te', gettext_noop('Telugu')),
    ('ur', gettext_noop('Urdu')),
]