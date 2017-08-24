from django.conf.urls import url
import views

urlpatterns=[
    url('^$',views.order),
    url('^pay(\d+)/$',views.pay),
]

