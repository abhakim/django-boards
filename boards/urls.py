from django.urls import path, re_path

from boards import views

urlpatterns = [
    # path('home/', views.home, name='home'),
    path('', views.BoardListView.as_view(), name='board_list'),
    # re_path(r'^$', views.board_list, name='board_list'),
    # re_path(r'^boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.reply_topic, name='reply'),
    re_path(r'^boards/(?P<pk>\d+)/$', views.TopicListView.as_view(), name='topic_list'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.PostListView.as_view(), name='post_list'),
    re_path(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    # re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.topic_posts, name='topic_posts'),
    re_path(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        views.PostUpdateView.as_view(), name='edit_post'),
    
]
