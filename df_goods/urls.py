from django.conf.urls import url
import views

urlpatterns=[
    url('^$',views.index),
    url('^index2(\d+)/$',views.index2),
    url('^list(\d+)_(\d+)_(\d)/$',views.list),
    url('^(\d+)/$',views.detail),
    url('^search/$',views.MySearchView()),
]
