import requests
from itertools import chain
from operator import attrgetter

from django.shortcuts import render, render_to_response, redirect
from django.http import JsonResponse, HttpResponse
from django.db.models import Q

from main.models import Event, Group, Profile, Comment, Notification

from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import ProfileSerializer, EventSerializer, GroupSerializer


class APIProfileList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get(self, request, format=None):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)


class APIFriends(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)


class APIProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class APIEventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)


class APIEventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)


class APIGroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)


class APIGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer


@api_view(['GET', 'POST'])
def api_friends(request):
    if not request.auth:
        return HttpResponse('Unauthorized', status=401)

    user = Token.objects.get(key=request.auth).user
    profile = Profile.objects.get(user=user)

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


@api_view(['GET', 'POST'])
def api_event_feed(request):

    if not request.user.is_authenticated():
        return HttpResponse('Unauthorized', status=401)

    profile = Profile.objects.get(user=request.user)

    # profile = Profile.objects.get(first_name="Ad")
    
    order = request.GET.get('order', '')

    return_dict = {}
    profile_dict = {}
    event_list = []

    return_dict['events'] = event_list
    return_dict['profile'] = profile_dict

    profile_dict['name'] = str(profile)
    profile_dict['username'] = profile.username
    profile_dict['id'] = profile.pk

    friend_events = []
    for friend in profile.friends.all():
        friend_events = list(chain(friend_events, friend.events_posted.filter(public=True)))

    group_events = []

    for group in profile.groups_in.all():
        group_events = list(chain(group_events, group.event_set.exclude(host=None)))

    friend_events = list(set(friend_events) | set(group_events))
    my_events = profile.events_posted.all()
    invited_events = profile.events_invited_to.all()
    my_events = list(set(my_events) | set(invited_events))

    if order:
        return_dict['order'] = True
        events = sorted(list(set(friend_events) | set(my_events)), key=attrgetter('date_posted'), reverse=True)
    else:
        return_dict['order'] = False
        events = sorted(list(set(friend_events) | set(my_events)), key=attrgetter('date_happening', 'time_starting')) #, reverse=True)


    for event in events:
        event_dict = {}
        event_dict['name'] = event.name
        event_dict['id'] = event.pk
        event_dict['description'] = event.description
        event_dict['date_posted'] = event.date_posted
        event_dict['date_happening'] = "%sT%s.000Z" % (event.date_happening, event.time_starting)
        event_dict['date_ending'] = "%sT%s.000Z" % (event.date_happening, event.time_ending)
        host_list = []
        for host in event.host.all():
            host_list.append({'host_pk': host.pk, 'img_url': host.picture.url, 'name': str(host)})
        event_dict['host'] = host_list
        group_list = []
        for group in event.groups.all():
            group_list.append({'group_pk': group.pk, 'name': group.name})
        event_dict['groups'] = group_list

        event_dict['people_coming'] = event.people_coming.count()
        event_dict['people_not_coming'] = event.people_not_coming.count()

        if profile.pk in event.host.values_list('pk', flat=True):
            event_dict['status'] = 'yourEvent'

        elif profile.pk in event.people_coming.values_list('pk', flat=True):
            event_dict['status'] = 'going'
        elif profile.pk in event.people_not_coming.values_list('pk', flat=True):
            event_dict['status'] = 'notGoing'
        else:
            event_dict['status'] = 'noDecision'
        event_list.append(event_dict)

    return JsonResponse(return_dict)


@api_view(['GET', 'POST'])
def api_group_event_feed(request):

    if not request.auth:
        return HttpResponse('Unauthorized', status=401)

    user = Token.objects.get(key=request.auth).user
    profile = Profile.objects.get(user=user)

    group_pk = request.GET.get('group_pk')
    group = Group.objects.get(pk=group_pk)

    if profile not in group.members.all():  
        return HttpResponse('No way Jose', status=403)

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


@api_view(['GET', 'POST'])
def api_facebook_friends(request):
    if not request.auth:
        return HttpResponse('Unauthorized', status=401)

    user = Token.objects.get(key=request.auth).user
    profile = Profile.objects.get(user=user)

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


@api_view(['GET', 'POST'])
def api_notifications(request):
    if not request.auth:
        return HttpResponse('Unauthorized', status=401)

    user = Token.objects.get(key=request.auth).user
    profile = Profile.objects.get(user=user)

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


@api_view(['GET', 'POST'])
def api_search_people(request):
    print request.auth
    print "dang it!"
    if not request.auth:
        return HttpResponse('Unauthorized', status=401)

    user = Token.objects.get(key=request.auth).user
    profile = Profile.objects.get(user=user)

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



def get_auth_token(request):
    return JsonResponse({'token': Token.objects.get(user=request.user).key})
