import requests

from django.shortcuts import render, render_to_response, redirect
from django.http import JsonResponse
from django.db.models import Q

from main.models import Event, Group, Profile, Comment, Notification

from rest_framework import generics, permissions
from .serializers import ProfileSerializer, EventSerializer, GroupSerializer


class APIProfileList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    

class APIFriends(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class APIProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class APIEventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class APIEventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class APIGroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class APIGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


def api_friends(request):
    user_pk = request.GET.get('user_pk')
    profile = Profile.objects.get(pk=user_pk)
    return_dict = {}
    profile_dict = {}
    friend_list = []

    return_dict['friends'] = friend_list
    return_dict['profile'] = profile_dict

    profile_dict['name'] = str(profile)
    profile_dict['username'] = profile.username
    profile_dict['id'] = profile.pk

    for friend in profile.friends.all():
        friend_dict = {}
        friend_dict['name'] = str(friend)
        friend_dict['id'] = friend.pk
        friend_dict['picture'] = friend.picture.url
        friend_dict['username'] = friend.username
        friend_list.append(friend_dict)

    return JsonResponse(return_dict)


def api_event_feed(request):
    user_pk = request.GET.get('user_pk')
    profile = Profile.objects.get(pk=user_pk)

    return_dict = {}
    profile_dict = {}
    event_list = []

    return_dict['events'] = event_list
    return_dict['profile'] = profile_dict

    profile_dict['name'] = str(profile)
    profile_dict['username'] = profile.username
    profile_dict['id'] = profile.pk


    for event in profile.events_posted.all():
        event_dict = {}
        event_dict['name'] = event.name
        event_dict['id'] = event.pk
        event_dict['description'] = event.description
        event_dict['date_posted'] = event.date_posted
        event_dict['date_happening'] = event.date_happening
        event_dict['time_starting'] = event.time_starting
        host_list = []
        for pk in event.host.values_list('pk', flat=True):
            host_list.append(pk)
        event_dict['host'] = host_list
        group_list = []
        for pk in event.groups.values_list('pk', flat=True):
            group_list.append(pk)
        event_dict['groups'] = group_list
        event_list.append(event_dict)

    return JsonResponse(return_dict)



def api_group_event_feed(request):
    group_pk = request.GET.get('group_pk')
    group = Group.objects.get(pk=group_pk)
    return_dict = {}
    group_dict = {}
    event_list = []
    return_dict['group'] = group_dict
    return_dict['events'] = event_list

    group_dict['name'] = group.name
    group_dict['id'] = group.pk

    for event in group.event_set.all():
        event_dict = {}
        event_dict['name'] = event.name
        event_dict['id'] = event.pk
        event_dict['description'] = event.description
        event_dict['date_posted'] = event.date_posted
        event_dict['date_happening'] = event.date_happening
        event_dict['time_starting'] = event.time_starting
        host_list = []
        for pk in event.host.values_list('pk', flat=True):
            host_list.append(pk)
        event_dict['host'] = host_list
        group_list = []
        for pk in event.groups.values_list('pk', flat=True):
            group_list.append(pk)
        event_dict['groups'] = group_list
        event_list.append(event_dict)

    return JsonResponse(return_dict)


def api_facebook_friends(request):

    user_pk = request.GET.get('user_pk')
    profile = Profile.objects.get(pk=user_pk)

    social = profile.user.social_auth.get(provider='facebook')
    response = requests.get('https://graph.facebook.com/v2.5/{0}/friends'.format(social.uid),params={'access_token': social.extra_data['access_token']})

    json = response.json()

    friends = json.get('data')
    friend_uid_list = []
    for friend in friends:
        friend_uid_list.append(friend.get('id'))

    friends = Profile.objects.filter(user__social_auth__uid__in=friend_uid_list)
    friends = friends.exclude(pk__in=profile.friends.values_list('pk', flat=True))

    return_dict = {}
    profile_dict = {}
    friend_list = []

    return_dict['friends'] = friend_list
    return_dict['profile'] = profile_dict

    profile_dict['name'] = str(profile)
    profile_dict['username'] = profile.username
    profile_dict['id'] = profile.pk


    for friend in friends:
        friend_dict = {}
        friend_dict['name'] = str(friend)
        friend_dict['id'] = friend.pk
        friend_dict['picture'] = friend.picture.url
        friend_dict['username'] = friend.username
        friend_list.append(friend_dict)

    return JsonResponse(return_dict)


def api_notifications(request):
    user_pk = request.GET.get('user_pk')
    profile = Profile.objects.get(pk=user_pk)

    return_dict = {}
    profile_dict = {}
    notification_list = []

    return_dict['notifications'] = notification_list
    return_dict['profile'] = profile_dict

    profile_dict['name'] = str(profile)
    profile_dict['username'] = profile.username
    profile_dict['id'] = profile.pk


    for notification in profile.notifications.all()[:20]:
        notification_dict = {}
        notification_dict['message'] = notification.message
        notification_dict['id'] = notification.pk
        notification_dict['notification_type'] = notification.notification_type
        notification_dict['date_notified'] = notification.date_notified
        notification_dict['read'] = notification.read
        notification_dict['sender_pk'] = notification.sender_pk
        notification_list.append(notification_dict)

    return JsonResponse(return_dict)



def api_search_people(request):

    user_pk = request.GET.get('user_pk')
    profile = Profile.objects.get(pk=user_pk)

    return_dict = {}
    profile_dict = {}
    profiles_list = []

    return_dict['search_results'] = profiles_list
    return_dict['profile'] = profile_dict

    profile_dict['name'] = str(profile)
    profile_dict['username'] = profile.username
    profile_dict['id'] = profile.pk

    search = request.GET.get('search', '').strip(' ')

    return_dict['search'] = search

    if " " in search:
        first, space, last = search.partition(' ')
        names = Profile.objects.filter(first_name__istartswith=first, last_name__istartswith=last)
    else:
        names = Profile.objects.filter(Q(first_name__istartswith=search) | Q(last_name__istartswith=search) )

    username = Profile.objects.filter(username__istartswith=search)
    result_list = list(set(names) | set(username))
    if profile in result_list:
        result_list.remove(profile)

    for search_result in result_list:
        search_result_dict = {}
        search_result_dict['name'] = str(search_result)
        search_result_dict['id'] = search_result.pk
        search_result_dict['picture'] = search_result.picture.url
        search_result_dict['username'] = search_result.username
        search_result_dict['is_friends'] = search_result.pk in profile.friends.values_list('pk', flat=True)
        profiles_list.append(search_result_dict)

    return JsonResponse(return_dict)