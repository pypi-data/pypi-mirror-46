from django.urls import reverse

def get_params_for_search(request, Obj, ObjForm, search_fields, result_fields):
    if not search_fields:
        search_fields = [field.name for field in Obj._meta.fields]
    fields = []
    charfield_exists = False
    datetimefield_exists = False
    booleanfield_exists = False 
    for field in search_fields: 
        internal_type = Obj._meta.get_field(field).get_internal_type()
        if internal_type in ('IntegerField', 'FloatField', 'DecimalField'):
            fields.append((field, 'number', 'ltgt'))
            charfield_exists = True
        elif internal_type in ('CharField', 'TextField'):
            fields.append((field, 'text', 'text'))
            charfield_exists = True
        elif internal_type in ('DateField', 'DateTimeField'):
            fields.append((field, 'date', 'ltgt'))
            datetimefield_exists = True
#        elif internal_type == 'ForeignKey':
#            fields.append((field, 'relation', 'relation'))
        elif internal_type == 'BooleanField':
            fields.append((field, 'boolean', 'text'))
            booleanfield_exists = True
    print(fields)
    class_name = Obj._meta.object_name
    class_name_lower = class_name.lower()
    ajax_url = reverse('ajax_get_%s_list' % class_name.lower())
    return (fields, class_name, class_name_lower, ajax_url, charfield_exists, \
            datetimefield_exists, booleanfield_exists)