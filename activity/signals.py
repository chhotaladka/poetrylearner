from django.dispatch import Signal

action = Signal(providing_args=['verb',
                                'content_type_id',
                                'object_id',
                                'object_repr',
                                'change_message',
                                'timestamp',
                                'public'])