from django.forms import ModelForm


class BaseForm(ModelForm):
    # Base class for all Repository ModelForm
    def __init__(self, *args, **kwargs):
        # Process the fields passed in kwargs, specifically related fields,
        # and exclude unwanted/invalid fields.
        # It will help to initialize the ModelForm fields to the values passed in `initial`.
        exclude_fields = []
        if kwargs.get('initial', None):
            for fieldname in kwargs.get('initial'):
                if fieldname not in self.Meta.fields:
                    # This is not in ModelForm fields, add to exclude list.
                    exclude_fields.append(fieldname)
                else:
                    # If the fieldname is a Related field (eg. Foreign Key), 
                    # then it's value must be converted to an integer, exclude otherwise
                    if self.Meta.model._meta.get_field(fieldname).is_relation:
                        # It's an Relation field
                        fk = kwargs.get('initial')[fieldname]
                        try:
                            kwargs.get('initial')[fieldname] = int(fk)
                        except (TypeError, ValueError):
                            # Exclude `fieldname`
                            exclude_fields.append(fieldname)
                            
            # Delete items of the exlcude_fields list from `initial`
            for fieldname in exclude_fields:
                del kwargs.get('initial')[fieldname]
        super(BaseForm, self).__init__(*args, **kwargs)
    
    