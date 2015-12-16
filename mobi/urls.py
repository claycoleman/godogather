from django.conf.urls import include, url

from mobi import views

from rest_framework.authtoken import views as token_views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^api/profile/list/$', views.APIProfileList.as_view()),
    url(r'^api/profile/(?P<pk>\d+)/$', views.APIProfileDetail.as_view()),
    url(r'^api/profile/friends/$', 'mobi.views.api_friends'),

    url(r'^api/event/list/$', views.APIEventList.as_view()),
    url(r'^api/event/(?P<pk>\d+)/$', views.APIEventDetail.as_view()),
    url(r'^api/feed/$', 'mobi.views.api_event_feed'),

    url(r'^api/group/list/$', views.APIGroupList.as_view()),
    url(r'^api/group/(?P<pk>\d+)/$', views.APIGroupDetail.as_view()),
    url(r'^api/feed/group/$', 'mobi.views.api_group_event_feed'),

    url(r'^api/facebook_friends/$', 'mobi.views.api_facebook_friends'),
    url(r'^api/notifications/$', 'mobi.views.api_notifications'),
    
    url(r'^api/search/people/$', 'mobi.views.api_search_people'),
    url(r'^get_auth_token/$', 'mobi.views.get_auth_token'),
    
    url(r'^api-token-auth/', token_views.obtain_auth_token),
]

urlpatterns = format_suffix_patterns(urlpatterns)
