from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^add_user$', views.add_user),
    url(r'^success$', views.success),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^tasks$',views.tasks),
    url(r'^python_add_user$', views.python_add_user),
]
