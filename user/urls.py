from django.conf.urls import url

from . import views

app_name = 'user'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register_user/$', views.register_user, name='register_user'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^search/$', views.search, name='search'),
    url(r'^query/$', views.query, name='query'),
    url(r'^homes/(?P<label>[\w]+)/$', views.dashboard, name='dashboard'),
    url(r'^homes/$', views.dashboard_folder, name='dashboard_folder'),
    url(r'^ajaxdashboard/$', views.ajax_dashboard, name='ajaxdashboard'),
    url(r'^ajaxtoggle/$', views.toggle, name='toggle'),
    url(r'^about/$', views.about, name='about'),
    url(r'^bibtexloads/$', views.bibtex, name='bibtex'),
    url(r'^checker/$', views.checker, name='checker'),
    url(r'^editpost/(?P<post_id>[0-9]+)/$', views.editpost, name='editpost'),
    url(r'^savepost/$', views.savepost, name='savepost'),
    url(r'^download/(?P<post_id>[0-9]+)/$', views.download, name='download'),
    url(r'^delete_doc/(?P<post_id>[0-9]+)/$', views.delete_doc, name='delete_doc'),
    url(r'^checklabel/$', views.check_label, name='check_label'),
    url(r'^createlabel/$', views.create_label, name='create_label'),
    url(r'^editlabel/(?P<label>[\w]+)/$', views.edit_folder, name='edit_folder'),
    url(r'^authanticate_delete/$', views.authenticates, name='authenticates'),

]
