from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^login$', views.log_in, name='login'),
    url(r'^register', views.register, name='register'),
    url(r'^activate/?', views.activate, name='activate'),
    url(r'^logout', views.log_out, name='logout'),
    url(r'^questions/tagged/(?P<tag_slug>[-\w]+)/(?P<page>[0-9]+)/$', views.questions, name='questions_by_tag'),
    # url(r'^questions/(?P<page>[0-9]+)/$', views.questions, name='questions'),
    url(r'^questions/$', views.questions, name='questions'),
    url(r'^question/(?P<qid>[0-9]+)$', views.question, name='question'),
    url(r'^tags/$', views.tags_view, name='tags'),
    url(r'^question$', views.question, name='question_ask'),
    url(r'^(?P<etype>[a-z]+)/(?P<eid>[0-9]+)/edit', views.general_edit, name='edit_question'),
    url(r'^edit_post/(?P<pid>[0-9]+)', views.edit_post, name='edit_post'),
    url(r'^react/(?P<rtype>[a-z]+)/(?P<rid>[0-9]+)/(?P<reaction>[a-z]+)$', views.react, name='react'),
    url(r'^react2/(?P<rtype>[a-z]+)/(?P<rid>[0-9]+)/(?P<reaction>[a-z]+)$', views.react2, name='react2'),
]
