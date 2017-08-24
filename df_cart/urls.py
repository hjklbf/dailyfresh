from django.conf.urls import url
import views

urlpatterns=[
    url('^$',views.list),
    url('^add(\d+)_(\d+)/$',views.add),
    url('^count_change/$',views.count_change),
    url('^delete/$',views.delete),
    url('^order/$',views.order),
]
