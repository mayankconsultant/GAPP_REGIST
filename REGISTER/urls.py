from django.urls import path

from . import views

from django.core.files.storage import FileSystemStorage, default_storage
from django.core.files.base import ContentFile

from django.urls import path, include
from django.views.generic import TemplateView
from .views import list, get_otp, load_COUNTY, load_PAYAM, cancel, detail, daybased, get_data, delete_msisdn

# app_name = 'REGISTER'
urlpatterns = [
    path('list/',
         list.as_view(template_name="register/list.html"), name="list"),
    path('list/<str:msisdn>',
         detail, name="list"),
    # path(   'new_register/',
    #             AllInOne.as_view()  ,        name="new_register"),
    path('',
         get_otp, name="new_register"),
    path('county/',
         load_COUNTY, name="load_COUNTY"),
    path('payam/',
         load_PAYAM, name="load_PAYAM"),
    path('cancel/',
         cancel, name="cancel"),
    path('list/<int:year>/<str:month>/<int:day>/',
         daybased.as_view(),
         name="archive_day"),
    path('json/get_data/<int:id>',
         get_data,
         name="api_get_data"),
    path('delete/<int:pk>',
         delete_msisdn.as_view(),
         name="delete_data"),
]
