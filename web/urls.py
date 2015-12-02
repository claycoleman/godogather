from django.conf.urls import include, url

urlpatterns = [

    # ajax urls
    url(r'^accept_request/$', 'web.views.accept_request'),
    url(r'^request_friendship/$', 'web.views.request_friendship'),
    url(r'^reject_request/$', 'web.views.reject_request'),
    url(r'^delete_friendship/$', 'web.views.delete_friendship'),
    url(r'^can_come/$', 'web.views.can_come'),
    url(r'^cannot_come/$', 'web.views.cannot_come'),
    url(r'^cancel_decision/$', 'web.views.cancel_decision'),
    url(r'^cancel_request/$', 'web.views.cancel_request'),
    url(r'^request_membership_in_group/$', 'web.views.request_membership_in_group'),
    url(r'^cancel_request_membership_in_group/$', 'web.views.cancel_request_membership_in_group'),
    url(r'^group_invitation_accepted/$', 'web.views.group_invitation_accepted'),
    url(r'^reject_invitation_from_group/$', 'web.views.reject_invitation_from_group'),
    url(r'^leave_group/$', 'web.views.leave_group'),

    # event urls
    url(r'^event_detail/(?P<pk>\d+)/$', 'web.views.event_detail_view', name='event_detail_view'),
    url(r'^$', 'web.views.event_list_view', name='event_list_view'),
    url(r'^event_delete/(?P<pk>\d+)/$', 'web.views.event_delete_view', name='event_delete_view'),
    url(r'^event_update/(?P<pk>\d+)/$', 'web.views.event_update_view', name='event_update_view'),
    url(r'^event_create/$', 'web.views.event_create_view', name='event_create_view'),
    # url(r'^search/events/$', 'web.views.search_events', name='search_events'),


    # group urls    
    url(r'^groups/$', 'web.views.group_list_view', name='group_list_view'),
    url(r'^groups/(?P<slug>.+)/events/$', 'web.views.group_event_list', name='group_event_list'),
    url(r'^groups/(?P<slug>.+)/$', 'web.views.group_detail_view', name='group_detail_view'),
    url(r'^group_delete/(?P<pk>\d+)/$', 'web.views.group_delete_view', name='group_delete_view'),
    url(r'^group_update/(?P<pk>\d+)/$', 'web.views.group_update_view', name='group_update_view'),
    url(r'^group_create/$', 'web.views.group_create_view', name='group_create_view'),
    # url(r'^search/groups/$', 'web.views.search_groups', name='search_groups'),


    # userprofile urls
    url(r'^profile_detail/(?P<pk>\d+)/$', 'web.views.profile_detail_view', name='profile_detail_view'),
    url(r'^profile_list/$', 'web.views.profile_list_view', name='profile_list_view'),
    url(r'^friends/$', 'web.views.friend_list', name='friend_list'),
    url(r'^search/profiles/$', 'web.views.search_profiles', name='search_profiles'),
    url(r'^profile_delete/(?P<pk>\d+)/$', 'web.views.profile_delete_view', name='profile_delete_view'),
    url(r'^profile_update/(?P<pk>\d+)/$', 'web.views.profile_update_view', name='profile_update_view'),
    url(r'^profile_create/$', 'web.views.profile_create_view', name='profile_create_view'),
    url(r'^notifications/$', 'web.views.full_notifications', name='full_notifications'),

    # permission urls
    url(r'^logout_view/$', 'web.views.logout_view', name='logout_view'),
    url(r'^home/$', 'web.views.new_user', name='new_user'),
    url(r'^about/$', 'web.views.about_view', name='about_view'),
    url(r'^contact/$', 'web.views.contact_view', name='contact_view'),
    url(r'^thank-you/$', 'web.views.thank_you', name='thank_you'),

]