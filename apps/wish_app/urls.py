from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration_success$', views.registration_success),
    url(r'^email$', views.email),
    url(r'^login_success$', views.login_success),
    url(r'^log_out$', views.log_out),
    url(r'^wishes$', views.wishes),
    url(r'^wishes/new$', views.wish_page),
    url(r'^create_new_wish$', views.create_new_wish),
    url(r'^wishes/edit/(?P<wish_id>\d+)$', views.edit_page),
    url(r'^wish_edit/(?P<wish_id>\d+)$', views.edit_wish),
    url(r'^remove_wish/(?P<wish_id>\d+)$', views.remove_wish),
    url(r'^grant_wish/(?P<wish_id>\d+)$', views.grant_wish),
    url(r'^like_wish/(?P<wish_id>\d+)$', views.like_wish),
    url(r'^wishes/stats$', views.stats),
]