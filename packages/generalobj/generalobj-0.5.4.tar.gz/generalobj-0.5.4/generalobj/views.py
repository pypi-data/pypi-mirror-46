from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse

import datetime, os, sys

from .utils import get_params_for_search

# Create your views here.


def general_obj_new(request, Obj, ObjForm, callback_prevalidation=False, \
        callback_postvalidation=False, \
        callback_postaction=False, callback_postsaveaction=False, \
        cancel_url=False, return_url=False, html_scripts=False, *args, **kwargs):
    """General form view for adding new objects
    
    It' s not a real view, rather a generic function to creating new objects with the predefined parameters:
    
        - name (the name of the Class)
        - callback_prevalidation (method, runs before form validation)
        - callback_postvalidation (method, runs after form validation)
        - callback_postaction (method, runs after saving the object with commit=False)
        - callback_postsaveaction (method, runs after saving the object)
        - cancel_url (string, in case of cancel, the user will be redirected to here)"""
    ret_dic = {}
    ret_dic['edit'] = False
    ret_dic['class_name'] = Obj._meta.object_name
    if html_scripts:
        ret_dic['html_scripts'] = html_scripts
    if request.method == 'POST':
        cancel = request.POST.get('cancel', '')
        if cancel:
#            request.session['info'] = ('You pressed the Cancel button', \
#            'You got redirected to somewhere')
            if cancel_url:
                return HttpResponseRedirect(cancel_url)
            else:
                if return_url:
                    return HttpResponseRedirect(return_url)
                else:
                    return HttpResponseRedirect(reverse("%ss" % \
                            ret_dic['class_name'].lower()))
        form = ObjForm(request.POST, request=request)
        if callback_prevalidation:
            form = callback_prevalidation(form)
        if form.is_valid():
            if callback_postvalidation:
                form = callback_postvalidation(form)
                if not form.is_valid():
                    ret_dic['form'] = ObjForm(request.POST, request=request)
                    request.session['err'] = []
                    for field, msg in form._errors.items():
                        request.session['err'].append('%s: %s' % (field, ' | '.join(msg)))
                    return render(request, 'generalobj_new.html', \
                           ret_dic)
            obj = form.save(commit=False)
            if callback_postaction:
                obj = callback_postaction(obj)
            obj.save()
            try:
                form.save_m2m()
            except AttributeError:
                pass
            if callback_postsaveaction:
                obj = callback_postsaveaction(obj)
                #TBF - it' s an ugly solution.
                #Hint: http://stackoverflow.com/questions/11137309/django-is-it-possible-to-make-a-redirect-from-a-function-in-a-view
                if type(obj) == HttpResponseRedirect:
                    return obj
            request.session['info'] = ['Saved']
            if return_url:
                return HttpResponseRedirect(return_url)
            return HttpResponseRedirect(reverse(ret_dic['class_name'].lower(), \
                    args=(obj.id,)))
        else:
            ret_dic['form'] = ObjForm(request.POST, request=request)
            return render(request, 'generalobj_new.html', \
                    ret_dic)
    else:
        ret_dic['form'] = ObjForm(request=request)
        return render(request, 'generalobj_new.html', ret_dic)

    return HttpResponse('qqq')


def general_obj_edit(request, Obj, ObjForm, general_obj_id, querysets=[], \
        callback_prevalidation=False, callback_postvalidation=False, \
        callback_postaction=False, callback_postsaveaction=False, \
        cancel_url=False, return_url=False):
    """General form view for editing a record of an object
    
        It' s not a real view, rather a generic function to edit objects with the predefined parameters:

            - name (the name of the Class)
            - general_obj_id (the id of the object)
            - queryset ()
            - callback_postvalidation (method, runs after form validation)
            - callback_postaction (method, runs after saving the object with commit=False)
            - callback_postsaveaction (method, runs after saving the object)
            - cancel_url (string, in case of cancel, the user will be redirected to here)"""
    ret_dic = {}
    ret_dic['edit'] = True
    ret_dic['class_name'] = Obj._meta.object_name
    obj = get_object_or_404(Obj, id=general_obj_id)
    ret_dic['delete_url'] = os.path.join(reverse(\
            ret_dic['class_name'].lower(), args=(obj.id,)), 'delete/')
    print(ret_dic)
    ret_dic['obj'] = obj
    if request.method == 'POST':
        cancel = request.POST.get('cancel', '')
        if not return_url:
            return_url = request.GET.get('return_url', '')
        if cancel:
#            request.session['info'] = ('You pressed the Cancel button',)
            if cancel_url:
                return HttpResponseRedirect(cancel_url)
            else:
                if return_url:
                    return HttpResponseRedirect(return_url)
                else:
                    return HttpResponseRedirect(reverse(\
                            ret_dic['class_name'].lower(), args=(obj.id,)))
        form = ObjForm(request.POST, instance=obj, request=request)
        if callback_prevalidation:
            form = callback_prevalidation(form)
            if isinstance(obj, HttpResponseRedirect):
                return obj
        if form.is_valid():
            if callback_postvalidation:
                form = callback_postvalidation(form)
                if not form.is_valid():
                    ret_dic['form'] = ObjForm(request.POST, instance=obj, request=request)
                    request.session['err'] = []
                    for field, msg in form._errors.items():
                        request.session['err'].append('%s: %s' % (field, ' | '.join(msg)))
                    return render(request, 'generalobj_new.html', \
                           ret_dic)
            obj = form.save(commit=False)
            if callback_postaction:
                obj = callback_postaction(obj)
            obj.save()
            try:
                form.save_m2m()
            except AttributeError:
                pass
            if callback_postsaveaction:
                obj = callback_postsaveaction(obj)
                if type(obj) == HttpResponseRedirect:
                    return obj
            request.session['info'] = ['Saved']
            if return_url:
                return HttpResponseRedirect(return_url)
            else:
#                return HttpResponseRedirect(reverse("%s_edit" % name.lower(), \
#                        args=(obj.id,)))
                return HttpResponseRedirect(reverse(\
                        ret_dic['class_name'].lower(), args=(obj.id,)))
        else:
            form = ObjForm(request.POST, instance=obj, request=request)
            ret_dic['form'] = form
            return render(request, 'generalobj_new.html', ret_dic)
    else:
        form = ObjForm(instance=obj, request=request)
        for qs in querysets:
            form.fields[qs[0]].queryset = qs[1]
        ret_dic['form'] = form
        return render(request, 'generalobj_new.html', ret_dic)


def general_obj_bulkedit(request, Obj, ObjForm, general_obj_ids, 
        callback_prevalidation=False, callback_postvalidation=False, \
        callback_postaction=False, callback_postsaveaction=False, \
        cancel_url=False, return_url=False, label=False, \
        editable_fields=False, allow_redirect_to_edit=True):
    ret_dic = {}
    ret_dic['edit'] = True
    ret_dic['class_name'] = Obj._meta.object_name
    ret_dic['label'] = label
    if general_obj_ids == 'all':
        objs = Obj.objects.filter()
    else:
        objs = Obj.objects.filter(id__in = general_obj_ids.split(','))
    #delete url
    ret_dic['objs'] = objs
    if len(objs) > 1:
        pass
    elif len(objs) == 1:
        if allow_redirect_to_edit:
            return HttpResponseRedirect(reverse(\
                    '%s_edit' % ret_dic['class_name'].lower(), \
                    args=(objs[0].id,)))
    else:
        pass
    ret_dic['ids_from_parameter'] = general_obj_ids
    if request.method == 'POST':
        cancel = request.POST.get('cancel', '')
        return_url = request.GET.get('return_url', '')
        if cancel:
            if cancel_url:
                return HttpResponseRedirect(cancel_url)
            else:
                if return_url:
                    return HttpResponseRedirect(return_url)
                else:
                    return HttpResponseRedirect(\
                            reverse('%ss' % ret_dic['class_name'].lower()))
        ret_dic['forms'] = []
        for obj in objs:
            form = ObjForm(request.POST, instance=obj, request=request, \
                    prefix='%s' % obj.id)
            if callback_prevalidation:
                form = callback_prevalidation(form)
                #We don' t want any redirection on a single form action
            obj_can_be_saved = True
            if form.is_valid():
                if callback_postvalidation:
                    form = callback_postvalidation(form)
                    if not form.is_valid():
                        obj_can_be_saved = False
                        #error handling should come here
                if obj_can_be_saved:
                    obj = form.save(commit=False)
                    if callback_postaction:
                        obj = callback_postaction(obj)
                    obj.save()
                    try:
                        form.save_m2m()
                    except AttributeError:
                        pass
                    if callback_postsaveaction:
                        obj = callback_postsaveaction(obj)
            else:
                print('x')
                pass
            formagain = ObjForm(request.POST, instance=obj, request=request, \
                    prefix='%s' % obj.id)
            ctrl = {}
            if hasattr(form, 'label_per_instance'):
                label_per_instance = form.label_per_instance
            else:
                label_per_instance = obj.__str__()
            ctrl['label_per_instance'] = label_per_instance
            ret_dic['forms'].append((formagain, ctrl))
        return render(request, 'generalobj_bulkedit.html', ret_dic)
    else:
        forms = []
        for obj in objs:
            form = ObjForm(instance=obj, request=request, prefix='%s' % obj.id)
            ctrl = {}
            if hasattr(form, 'label_per_instance'):
                label_per_instance = form.label_per_instance
            else:
                label_per_instance = obj.__str__()
            ctrl['label_per_instance'] = label_per_instance
            forms.append((form, ctrl))
        ret_dic['forms'] = (forms)
        return render(request, 'generalobj_bulkedit.html', ret_dic)
                
        
    

def general_obj_delete(request, name, general_obj_id):
    try:
        Obj = eval(name)
    except NameError:
        pass
    try:
        obj = Obj.objects.get(id=general_obj_id)
        obj.delete()
        request.session['info'] = ('%s#%s has been deleted: %s' % \
                (name, general_obj_id, obj.__dict__),)
    except:
        request.session['err'] = ('%s#%s is not deletable: %s' % \
                (name, general_obj_id, sys.exc_info()[0]),)
    return HttpResponseRedirect(reverse('index'))


def general_objs(request, Obj, ObjForm, fields=(), query_dict={}, query_term='', \
        excluded_query_dict={}, no_id_in_fields=False, \
        show_unused_download_excelsheet_button=False, *args, **kwargs):
    """General view for displaying records of an object
    
    It' s not a real view, rather a generic function to displaying filtered list of an Object with a datatable.
    
    The parameters are:
    
        - name (the name of the Class)
        - fields (the fields to be displayed [overrides the default values])
        - query_dict (dictionary for **query)
        - query_term (term for query)
        - excluded_query_dict (dictionary for .exclude(**excluded_query_dict))"""
    ret_dic = {}
    ret_dic['class_name'] = Obj._meta.object_name
    ret_dic['show_unused_download_excelsheet_button'] = \
            show_unused_download_excelsheet_button
    if not fields and not fields == 'DONTDOIT':
        field_names = [field.name for field in Obj._meta.fields]
    else:
        field_names = ['id'] + fields
    if no_id_in_fields:
        field_names.remove('id')
    objs = Obj.objects.filter(**query_dict).exclude(**excluded_query_dict)
    if query_term:
        objs = objs.filter(query_term)
    objs = objs.distinct()
    ret_dic['all_id'] = ','.join([str(obj.id) for obj in objs])
    ret_dic['obj_name'] = ret_dic['class_name']
    fields = []
    obj_name_html = False
    obj_name_html_path = os.path.join(Obj._meta.app_config.path, 'templates', \
            'blocks', '%s_name.html' % ret_dic['class_name'].lower())
    if os.access(obj_name_html_path, os.R_OK):
        obj_name_html = obj_name_html_path
    field_htmls = {}
    for field_name in field_names:
        _field_html = os.path.join(Obj._meta.app_config.path, 'templates', \
                'blocks', '%s_name.html' % field_name)
        if os.access(_field_html, os.R_OK):
            field_htmls[field_name] = _field_html
    for obj in objs:
        if no_id_in_fields:
            field = []
        else:
            if obj_name_html:
                field = [render_to_string(obj_name_html, {ret_dic['obj_name'].lower(): obj})]
            else:
                field = ["<A href='%s'>%s</A>" % (\
                        reverse(ret_dic['class_name'].lower(), \
                        args=(obj.id,)), obj.id)]
        for field_name in field_names:
            if not field_name == 'id':
                if not field_name in field_htmls:
                    field.append(getattr(obj, field_name))
                else:
                    field.append(render_to_string(field_htmls[field_name], {ret_dic['obj_name'].lower(): obj}))
        fields.append(field)
    ret_dic['field_names'] = field_names
    ret_dic['fields'] = fields
    ret_dic['objs'] = Obj.objects.filter()
    if not no_id_in_fields:
        ret_dic['url_new'] = reverse('%s_new' % ret_dic['class_name'].lower())
    ret_dic['url_tag'] = ret_dic['class_name'].lower()
    if 'additional_template' in kwargs:
        ret_dic['additional_template'] = kwargs['additional_template']
    if 'pass_to_template' in kwargs:
        for name, value in kwargs['pass_to_template'].items():
            ret_dic[name] = value
    return render(request, 'generalobjs.html', ret_dic)


def general_obj(request, Obj, ObjForm, general_obj_id, fields=(), \
        template=False, html_scripts=False, *args, **kwargs):
    """General view for displaying a detailed view of an object"""
    if not template:
        template = 'generalobj.html'
    ret_dic = {}
    if html_scripts:
        ret_dic['html_scripts'] = html_scripts
    obj = get_object_or_404(Obj, id=general_obj_id)
    ret_dic['obj'] = obj
    ret_dic['class_name'] = Obj._meta.object_name
    if not fields:
        fields = [field.name for field in obj._meta.fields]
    if fields:
        ret_dic['fields'] = []
        for field in fields:
            ret_dic['fields'].append((field, getattr(obj, field)))
    ret_dic['url_edit'] = reverse('%s_edit' % ret_dic['class_name'].lower(), \
            args=(obj.id,))
    if 'additional_tabs' in kwargs:
        ret_dic['additional_tabs'] = kwargs['additional_tabs']
    if 'pass_to_template' in kwargs:
        for name, value in kwargs['pass_to_template'].items():
            ret_dic[name] = value
    return render(request, template, ret_dic)


def general_obj_search(request, Obj, ObjForm, search_fields=(), \
        result_fields=(), template=False):
    if not template:
        template = 'generalobj_search.html'
    ret_dic = {}
    (ret_dic['fields'], ret_dic['class_name'], ret_dic['class_name_lower'], \
            ret_dic['ajax_url'], ret_dic['charfield_exists'], \
            ret_dic['datetimefield_exists'], ret_dic['booleanfield_exists']) = \
            get_params_for_search(request, Obj, ObjForm, search_fields, \
            result_fields)
    return render(request, template, ret_dic)


def ajax_get_general_obj_list(request, Obj, ObjForm, search_fields=(), \
        result_fields=()):
    (fields, class_name, class_name_lower, ajax_url, charfield_exists, \
            datetimefield_exists, booleanfield_exists) = \
            get_params_for_search(request, Obj, ObjForm, search_fields, \
            result_fields)
    class_names_lower = '%ss' % class_name_lower

    ret_dic = {}
    if not result_fields:
        result_fields = [field.name for field in Obj._meta.fields]
    get_fields = {}
    print(fields)
    for field in fields:
        if field[2] == 'ltgt':
            get_fields['%s_gt' % field[0]] = request.GET.get(\
                    '%s_gt' % field[0], '')
            get_fields['%s_lt' % field[0]] = request.GET.get(\
                    '%s_lt' % field[0], '')
        elif field[2] == 'text':
            get_fields[field[0]] = request.GET.get(field[0], '').strip()
    print('gf = ', get_fields)
    useful_data_available = False
    useful_data_available = any([item[1] for item in get_fields.items()])
    print('uf = ', useful_data_available)
    if useful_data_available:
        dt = {}
        for field in fields:
            if field[1] == 'number':
                if get_fields['%s_gt' % field[0]]:
                    dt['%s__gte' % field[0]] = get_fields['%s_gt' % field[0]]
                if get_fields['%s_lt' % field[0]]:
                    dt['%s__lte' % field[0]] = get_fields['%s_lt' % field[0]]
            elif field[1] == 'text':
                if get_fields[field[0]]:
                    dt['%s__icontains' % field[0]] = \
                            get_fields[field[0]].strip()
            elif field[1] == 'date':
                if get_fields['%s_gt' % field[0]]:
                    dt['%s__gte' % field[0]] = datetime.datetime.strptime(\
                            get_fields['%s_gt' % field[0]], '%d/%m/%Y')
                if get_fields['%s_lt' % field[0]]:
                    dt['%s__lte' % field[0]] = datetime.datetime.strptime(\
                            get_fields['%s_lt' % field[0]], '%d/%m/%Y')
            elif field[1] == 'boolean':
                if get_fields[field[0]]:
                    TRUE = 'true' in get_fields[field[0]].split(',')
                    FALSE = 'false' in get_fields[field[0]].split(',')
                    if TRUE and FALSE:
                        pass
                    elif TRUE:
                        dt[field[0]] = True
                    else:
                        dt[field[0]] = False
        ret_dic['objects'] = Obj.objects.filter(**dt)
        print('dt = %s' % dt)
    else:
        ret_dic['objects'] = Obj.objects.all()
    print(request.GET)
    ret_dic['all_id'] = ','.join([str(obj.id) for obj in \
            ret_dic['objects']])
    ret_dic['result_fields'] = result_fields
    return render(request, 'ajax/get_object_list.html', ret_dic)
    print(dt)
    print('xx', useful_data_available)


def download_excelsheet(request):
    print(request.POST)
    pass