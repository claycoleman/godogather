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
    url(r'^user_accepts_invitation/$', 'web.views.user_accepts_invitation'),
    url(r'^group_approves_request/$', 'web.views.group_approves_request'),
    url(r'^reject_invitation_from_group/$', 'web.views.reject_invitation_from_group'),
    url(r'^leave_group/$', 'web.views.leave_group'),
    url(r'^clear_notification/$', 'web.views.clear_notification'),
    url(r'^ajax/friends/$', 'web.views.ajax_friends'),
    url(r'^ajax/facebook_friends/$', 'web.views.ajax_facebook_friends'),
    url(r'^invite_friend_to_group/$', 'web.views.invite_friend_to_group'),
    url(r'^share_event/$', 'web.views.share_event'),
    url(r'^subscribe/(?P<pk>\d+)/$', 'web.views.subscribe', name='subscribe'),
    url(r'^subscribe_group/(?P<pk>\d+)/$', 'web.views.subscribe_group', name='subscribe_group'),
    url(r'^add_friend_to_friend_list/$', 'web.views.add_friend_to_friend_list'),
    url(r'^invite_friend_to_event/$', 'web.views.invite_friend_to_event'),
    url(r'^invite_friend_list_to_event/$', 'web.views.invite_friend_list_to_event'),
    url(r'^mark_non_new_user/$', 'web.views.mark_non_new_user'),
    url(r'^search_invite_event_json/(?P<pk>\d+)/$', 'web.views.search_invite_event_json'),
    url(r'^search_invite_group_json/(?P<pk>\d+)/$', 'web.views.search_invite_group_json'),

    # event urls
    url(r'^events/(?P<pk>\d+)/$', 'web.views.event_detail_view', name='event_detail_view'),
    url(r'^home/$', 'web.views.event_list_view', name='event_list_view'),
    url(r'^events/delete/(?P<pk>\d+)/$', 'web.views.event_delete_view', name='event_delete_view'),
    url(r'^events/update/(?P<pk>\d+)/$', 'web.views.event_update_view', name='event_update_view'),
    url(r'^events/create/$', 'web.views.event_create_view', name='event_create_view'),
    url(r'^invite_friends_to_event/(?P<pk>\d+)/$', 'web.views.invite_friends_to_event_view', name='invite_friends_to_event_view'),
    url(r'^invite_friend_lists_to_event/(?P<pk>\d+)/$', 'web.views.invite_friend_lists_to_event_view', name='invite_friend_lists_to_event_view'),
    url(r'^share_buttons/(?P<pk>\d+)/$', 'web.views.share_buttons', name='share_buttons'),
    url(r'^calendar_buttons/(?P<pk>\d+)/$', 'web.views.calendar_buttons', name='calendar_buttons'),
    # url(r'^search/events/$', 'web.views.search_events', name='search_events'),


    # group urls    
    url(r'^groups/$', 'web.views.group_list_view', name='group_list_view'),
    url(r'^groups/(?P<pk>\d+)/$', 'web.views.group_event_list', name='group_event_list'),
    url(r'^groups/(?P<pk>\d+)/members/$', 'web.views.group_member_view', name='group_member_view'),
    url(r'^groups/(?P<pk>\d+)/delete/$', 'web.views.group_delete_view', name='group_delete_view'),
    url(r'^groups/(?P<pk>\d+)/update/$', 'web.views.group_update_view', name='group_update_view'),
    url(r'^groups/create/$', 'web.views.group_create_view', name='group_create_view'),
    # url(r'^search/groups/$', 'web.views.search_groups', name='search_groups'),


    # friendlist urls
    url(r'^friends/list/(?P<pk>\d+)/$', 'web.views.friend_list_detail_view', name='friend_list_detail_view'),
    url(r'^friend/list/(?P<pk>\d+)/delete/$', 'web.views.friend_list_delete_view', name='friend_list_delete_view'),
    url(r'^pick_friends_for_list/(?P<pk>\d+)/$', 'web.views.pick_friends_for_list', name='pick_friends_for_list'),



    # userprofile urls
    url(r'^people/(?P<pk>\d+)/$', 'web.views.profile_detail_view', name='profile_detail_view'),
    url(r'^friends/$', 'web.views.friend_list', name='friend_list'),
    url(r'^search/profiles/$', 'web.views.search_profiles', name='search_profiles'),
    url(r'^profile/(?P<pk>\d+)/update/$', 'web.views.profile_update_view', name='profile_update_view'),
    url(r'^profile/create/$', 'web.views.profile_create_view', name='profile_create_view'),
    url(r'^notifications/$', 'web.views.full_notifications', name='full_notifications'),

    # permission urls
    url(r'^logout_view/$', 'web.views.logout_view', name='logout_view'),
    url(r'^$', 'web.views.new_user', name='new_user'),
    url(r'^about/$', 'web.views.about_view', name='about_view'),
    url(r'^contact/$', 'web.views.contact_view', name='contact_view'),
    url(r'^thank-you/$', 'web.views.thank_you', name='thank_you'),

    # comment urls
    url(r'^delete/comment/(?P<pk>\d+)/$', 'web.views.comment_delete_view', name='comment_delete_view')

]