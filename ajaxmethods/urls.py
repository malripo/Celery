from django.urls import path
from . views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('', home_page, name="ajax"),
    path('vanilla/', TemplateView.as_view(template_name="ajaxmethods/vanilla.html"), name='vanilla'),
    path('fetch/', TemplateView.as_view(template_name="ajaxmethods/fetch.html"), name='fetch'),
    path('fetchawait/', TemplateView.as_view(template_name="ajaxmethods/fetchawait.html"), name='fetchawait'),
    path('axios/', TemplateView.as_view(template_name="ajaxmethods/axios.html"), name='axios'),
    path('jQuery/', TemplateView.as_view(template_name="ajaxmethods/jQuery.html"), name='jQuery'),
    path('htmx/', TemplateView.as_view(template_name="ajaxmethods/htmx.html"), name='htmx'),    
    path('json-data/', json_data, name='json-data'),
    path('html-data/', html_data, name='html-data'),
]