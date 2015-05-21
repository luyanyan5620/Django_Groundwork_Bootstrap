# -------------------- #
# urls.py file section #
# -------------------- #


URL_IMPORTS = """
from django.conf.urls import patterns, url, include
from .models import *
from .views import *

urlpatterns = patterns('',
"""

URL_CRUD_CONFIG = """
    (r'%(model)s/create/$', create_%(model)s),
    (r'%(model)s/list/$', list_%(model)s ),
    (r'%(model)s/edit/(?P<id>[^/]+)/$', edit_%(model)s),
    (r'%(model)s/view/(?P<id>[^/]+)/$', view_%(model)s),
    (r'%(model)s/del/(?P<id>[^/]+)/(?P<page>\d+)$', del_%(model)s),
    """ 

URL_END = """
)
"""



# --------------------- #
# forms.py file section #
# --------------------- #

FORMS_IMPORTS = """
from django import forms
from .models import *

"""

FORMS_MODELFORM_CONFIG = """

class %(modelClass)sForm(forms.ModelForm):
	
    class Meta:
        model = %(modelClass)s
        fields = "__all__"
        # exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(%(modelClass)sForm, self).__init__(*args, **kwargs)

"""		





# --------------------- #
# views.py file section #
# --------------------- #

VIEWS_IMPORTS = """
# Create your views here.

from django import forms
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

# app specific files

from .models import *
from .forms import *
"""

VIEWS_CREATE = """

def create_%(model)s(request):

    form = %(modelClass)sForm(request.POST or None)

    if form.is_valid():
        form.save()
        form = %(modelClass)sForm()

    t = get_template('%(app)s/create_%(model)s.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))

"""

VIEWS_LIST = """

def list_%(model)s(request):
  
    list_items = %(modelClass)s.objects.all()
    paginator = Paginator(list_items, 10)

    if hasattr(%(modelClass)s, 'list_display'):
        show_field = %(modelClass)s.list_display
    else:
        show_field = ('id',)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)

    t = get_template('%(app)s/list_%(model)s.html')
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))

"""


VIEWS_UPDATE = """
def edit_%(model)s(request, id):

    %(model)s_instance = %(modelClass)s.objects.get(id=id)

    form = %(modelClass)sForm(request.POST or None, instance = %(model)s_instance)

    if form.is_valid():
        form.save()

    t=get_template('%(app)s/edit_%(model)s.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))
"""

VIEWS_VIEW = """

def view_%(model)s(request, id):

    %(model)s_instance = %(modelClass)s.objects.get(id = id)

    if hasattr(%(modelClass)s, 'list_display'):
        show_field = %(modelClass)s.list_display
    else:
        show_field = ('id',)

    t=get_template('%(app)s/view_%(model)s.html')
    c=RequestContext(request,locals())
    return HttpResponse(t.render(c))
"""

VIEWS_DEL = """

def del_%(model)s(request, id, page):

    %(modelClass)s.objects.filter(id=id).delete()

    return redirect('/%(app)s/%(model)s/list/?page='+page)
"""


# ------------------------- #
# templates.py file section #
# ------------------------- #



TEMPLATES_CREATE = """
{%% extends "base.html" %%}
{%% load bootstrap3 %%}
{%% block title %%} %(modelClass)s - Create {%% endblock %%}

{%% block heading %%}<h1>  %(modelClass)s - Create </h1>  {%% endblock %%}
{%% block content %%}
<form role="form" class="form-horizontal" action="" method="POST"> {%% csrf_token %%}
  {%% bootstrap_form form layout='horizontal' %%}
  {%% buttons submit='OK' reset='Cancel' layout='horizontal' %%}{%% endbuttons %%}
</form>
{%% endblock %%}
"""

TEMPLATES_LIST = """
{%% extends "base.html" %%}
{%% load getattribute %%}
{%% load bootstrap3 %%}
{%% block title %%} <h1> %(modelClass)s </h1><h2> List </h2> {%% endblock %%}

{%% block heading %%} 
<h1> %(modelClass)s - List Records </h1>
{%% endblock %%}
{%% block content %%} 

<table class="table table-striped table-hover">
<thead>
<tr>
    {%% for field in show_field %%}
    <th>{{ field }}</th>
    {%% endfor %%}
    <th colspan="3">Actions</th>
</tr>
</thead>
{%% for item in list_items.object_list %%}
  <tr>
      {%% for field in show_field %%}
        <td>{{ item|getattribute:field }}</td>
      {%% endfor %%}
      <td><a class="btn btn-success" role="button" href="{%% url "%(app)s.views.view_%(model)s" item.id %%}">Show</a> </td> <td><a class="btn btn-warning" role="button" href="{%% url "%(app)s.views.edit_%(model)s" item.id %%}">Edit</a></td><td><a class="btn btn-danger" role="button" href="{%% url "%(app)s.views.del_%(model)s" item.id list_items.number %%}">Del</a></td></tr>
{%% endfor %%}
<tr><td colspan="4"> <a class="btn btn-primary" role="button" href="{%% url "%(app)s.views.create_%(model)s" %%}">Add New</a></td></tr>
</table>

<div align="center">
<nav>
  <ul class="pagination">
    {%% if list_items.has_previous %%}
        <li><a aria-label="Previous" href="?page={{ list_items.previous_page_number }}">
            <span aria-hidden="true">Previous</span>
        </a></li>
    {%% endif %%}

      {%% for number in list_items.paginator.page_range %%}
          {%% if list_items.number == number %%}
              <li class="active"><a href="#">{{ number }}<span class="sr-only">(current)</span></a></li>
          {%% else %%}
              <li><a href="?page={{ number }}">{{ number }}</a></li>
          {%% endif %%}
      {%% endfor %%}


    {%% if list_items.has_next %%}
        <li><a aria-label="Next" href="?page={{ list_items.next_page_number }}">
            <span aria-hidden="true">Next</span>
        </a></li>
    {%% endif %%}
  </ul>
</nav>
</div>

{%% endblock %%}
"""


TEMPLATES_EDIT = """
{%% extends "base.html" %%}
{%% load bootstrap3 %%}
{%% block title %%} %(modelClass)s - Edit {%% endblock %%}

{%% block heading %%} <h1> %(modelClass)s -Edit </h1>{%% endblock %%}
{%% block content %%} 
<form role="form" class="form-horizontal" action="" method="POST">
    {%% csrf_token %%}
    {%% bootstrap_form form layout='horizontal' %%}
    {%% buttons submit='OK' reset='Cancel' layout='horizontal' %%}{%% endbuttons %%}
</form>
{%% endblock %%}
"""

TEMPLATES_VIEW = """
{%% extends "base.html" %%}
{%% load getattribute %%}
{%% load bootstrap3 %%}
{%% block title %%} %(modelClass)s - View {%% endblock %%}

{%% block heading %%} <h1> %(modelClass)s - View</h1>{%% endblock %%}
{%% block content %%} 
<table class="table table-hover">
<thead>
    {%% for field in show_field %%}
    <th>{{ field }}</th>
    {%% endfor %%}
</thead>
<tr>
      {%% for field in show_field %%}
        <td>{{ %(model)s_instance|getattribute:field }}</td>
      {%% endfor %%}
</tr>
</table>
{%% endblock %%}
"""

TEMPLATES_BASE = """
{% extends 'bootstrap3/bootstrap3.html' %}

{% load url from future %}

{% load bootstrap3 %}
{% block title %}(no title){% endblock %}
{% block bootstrap3_content %}
    <div class="container">
        <h1>{% block heading %}(no heading){% endblock %}</h1>

        <p>

        </p>

        {% bootstrap_messages %}
        {% block content %}(no content){% endblock %}
        {% block footer %}
            <hr/><p style='color:#000'>Power by Lianzk</p>
        {% endblock %}
    </div>
{% endblock %}
"""

TEMPLATE_TAGS = """
import re
from django import template
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = template.Library()

def getattribute(value, arg):
    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return settings.TEMPLATE_STRING_IF_INVALID

register.filter('getattribute', getattribute)
"""

