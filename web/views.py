import pytz, requests, urllib
from itertools import chain
from operator import attrgetter
from datetime import datetime

from django.shortcuts import render, render_to_response, redirect, resolve_url
from django.http import JsonResponse
from django.utils import timezone
from django.template import RequestContext
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from project.local import FB_APP_ID
from sorl.thumbnail import get_thumbnail


from main.models import Event, Group, Profile, Comment, Notification, FriendList
from main.forms import SearchProfile, EventModelCreateForm, EventModelUpdateForm, GroupModelCreateForm, GroupModelUpdateForm, UserLogin, ProfileModelCreateForm, ProfileModelUpdateForm, GroupModelCreateForm, GroupModelUpdateForm, ContactForm, CommentForm, FriendListCreate



#  Event Views!

@login_required
def event_detail_view(request, pk):
    events = [e for e in Event.objects.filter(pk=pk)]
    if events:
        event = events[0]
    else:
        return redirect('{}?fail=eventremoved'.format(resolve_url('event_list_view')))

    comments = event.comment_set.all().order_by('-date_posted')
    context = {}

    context['invitees'] = event.invitees.exclude(Q(pk__in=event.people_coming.values_list('pk', flat=True)) | Q(pk__in=event.people_not_coming.values_list('pk', flat=True)))
    # TO DO -- fix the redirect-uri
    
    
    context['date_ending'] = datetime.combine(date=event.date_happening, time=event.time_ending).isoformat('T')
    
    context['comments'] = comments
    context['event'] = event
    context['friends'] = list(request.user.profile.friends.all())
    form = CommentForm()
    context['form'] = form
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            if message != "":
                new_comment = Comment.objects.create(message=message)
                new_comment.author = request.user.profile
                new_comment.event = event

                reply_pk = request.POST.get('reply-pk')
                if reply_pk != '':
                    parent = Comment.objects.get(pk=reply_pk)
                    new_comment.comment_in_response_to = parent
                    parent.save()

                    reply_pks = []
                    parent_notified = False
                    for reply in parent.replies.all():
                        if reply.author != request.user.profile and reply.author.pk not in reply_pks:
                            if reply.author == parent.author:
                                parent_notified = True    
                            reply_pks.append(reply.author.pk)
                            new_notif = Notification.objects.create(user=reply.author)
                            new_notif.notification_type = "Reply to same comment on event"
                            new_notif.message = "%s also replied to a comment you replied to. %s." % (request.user.profile.first_name, event.name)
                            new_notif.sender_pk = event.pk
                            new_notif.save()

                    if not parent_notified and parent.author != request.user.profile:
                        new_notif = Notification.objects.create(user=parent.author)
                        new_notif.notification_type = "Reply to your comment on event"
                        new_notif.message = "%s replied to your comment on the event %s." % (request.user.profile.first_name, event.name)
                        new_notif.sender_pk = event.pk
                        new_notif.save()

                new_comment.save()

                for host in event.host.exclude(pk=request.user.profile.pk):
                    if host.notifications.filter(read=False, sender_pk=event.pk, notification_type__istartswith='Comment on').exists():
                        notif = host.notifications.get(read=False, sender_pk=event.pk, notification_type__istartswith='Comment on')

                        if 'multiple' not in notif.notification_type:
                            prev_pk = notif.notification_type.partition('event ')[2]

                            if request.user.profile.pk != prev_pk:
                                notif.message = "%s and 1 other person commented on your event %s." % (request.user.profile.first_name, event.name)
                                notif.notification_type = "Comment on your event multiple %s" % request.user.profile.pk
                            else:
                                notif.message = "%s commented on your event %s." % (request.user.profile.first_name, event.name)
                                notif.notification_type = "Comment on your event %s" % (request.user.profile.pk)

                        else:
                            prev_pk = notif.notification_type.partition('multiple ')[2]

                            if request.user.profile.pk != prev_pk:
                                notif.message = "%s and other people commented on your event %s." % (request.user.profile.first_name, event.name)
                                notif.notification_type = "Comment on your event multiple %s" % request.user.profile.pk

                        notif.date_posted = datetime.now()
                        notif.save()
                    else:
                        new_notif = Notification.objects.create(user=host)
                        new_notif.notification_type = "Comment on your event %d" % request.user.profile.pk
                        new_notif.message = "%s commented on your event %s." % (request.user.profile.first_name, event.name)
                        new_notif.sender_pk = event.pk
                        new_notif.save()
                return redirect('{}#comment-section'.format(resolve_url('event_detail_view', pk=pk)))

    return render_to_response('event_detail.html', context, context_instance=RequestContext(request))


@login_required
def event_list_view(request):

    context = {}
    context['friends_pk'] = request.user.profile.friends.values_list('pk', flat=True)
    context['groups_in'] = request.user.profile.groups_in.values_list('pk', flat=True)

    order = request.GET.get('order', '')
    fail = request.GET.get('fail', '')
    if 'eventremoved' in fail:
        context['fail'] = "Sorry, the event you're looking for has been deleted, or doesn't exist!"
    elif 'groupremoved' in fail:
        context['fail'] = "Sorry, the group you're looking for has been deleted, or doesn't exist!"
    elif 'listremoved' in fail:
        context['fail'] = "Sorry, the friend list you're looking for has been deleted, or doesn't exist!"

    friend_events = []
    for friend in request.user.profile.friends.all():
        friend_events = list(chain(friend_events, friend.events_posted.filter(public=True)))

    group_events = []

    for group in request.user.profile.groups_in.all():
        group_events = list(chain(group_events, group.event_set.all()))

    friend_events = list(set(friend_events) | set(group_events))
    my_events = request.user.profile.events_posted.all()
    invited_events = request.user.profile.events_invited_to.all()
    my_events = list(set(my_events) | set(invited_events))

    if order:
        context['order'] = True
        events = sorted(list(set(friend_events) | set(my_events)), key=attrgetter('date_posted'), reverse=True)
    else:
        events = sorted(list(set(friend_events) | set(my_events)), key=attrgetter('date_happening', 'time_starting')) #, reverse=True)

    for event in events:
        event_date = datetime.combine(date=event.date_happening, time=event.time_starting)
        
        timezone_inst = ""
        if not timezone_inst:
            timezone_inst = 'UTC'

        event_date = event_date.replace(tzinfo=pytz.timezone(timezone_inst))
        if event_date < timezone.now():
            for host in event.host.all():
                host.events_hosted.remove(event)
                host.past_events.add(event)
            event.people_coming.clear()
            event.people_not_coming.clear()
            event.people_who_posted_it.clear()
            event.people_who_shared_it.clear()
            try:
                os.remove(event.ics.file.name)
            except:
                pass
            events.remove(event)

    context['today'] = datetime.now()
    context['events'] = events
    context['my_events'] = my_events

    return render_to_response('event_list.html', context, context_instance=RequestContext(request))
    

@login_required
def event_create_view(request):
    context = {} 

    friends = request.user.profile.friends.all()
    groups = request.user.profile.groups_in.filter(admin_only=False)
    admin_groups = request.user.profile.groups_in.filter(admin_only=True, admin=request.user.profile)
    
    groups = groups | admin_groups    
    
    if request.method == 'POST':
        pk = request.POST.get('event_pk')
        context['event_pk'] = pk
        event_saved = Event.objects.get(pk=pk)
        form = EventModelCreateForm(request.POST, instance=event_saved)
        if form.is_valid():
            should_save = True
            new_event = form.save(commit=False)
            print "New event: %s" % new_event.pk
            event = datetime.combine(new_event.date_happening, new_event.time_starting)
            event_ending = datetime.combine(new_event.date_happening, new_event.time_ending)

            timezone_inst = form.data['timezone']
            if not timezone_inst:
                timezone_inst = 'UTC'
                print "UTC'd"
            event = event.replace(tzinfo=pytz.timezone(timezone_inst))
            event = event.astimezone(pytz.utc)
            event_ending = event_ending.replace(tzinfo=pytz.timezone(timezone_inst))
            event_ending = event_ending.astimezone(pytz.utc)

            
            if event < timezone.now():
                should_save = False
                context['errors'] = "The event date was already in the past! Try again."
                form = EventModelCreateForm(initial=return_dict(form.data))
                form.fields['groups'].queryset = groups
                form.fields['host'].queryset = friends
                context['form'] = form

            if should_save:
                new_event.date_happening = event.date()
                new_event.time_starting = event.time()
                new_event.time_ending = event_ending.time()
                new_event.save()
                form.save_m2m()
                new_event.host.add(request.user.profile)
                for host in new_event.host.all():
                    new_event.people_coming.add(host)
                    host.events_posted.add(new_event)
                    for follower in host.followers.all():
                        new_notif = Notification.objects.create(user=follower)
                        new_notif.notification_type = "Following posted event"
                        new_notif.message = "%s posted a new event, \"%s\"." % (host.first_name, new_event.name)
                        new_notif.sender_pk = new_event.pk
                        new_notif.save()
                for group in new_event.groups.all():
                    for follower in group.followers.all():
                        new_notif = Notification.objects.create(user=follower)
                        new_notif.notification_type = "Following group posted event"
                        new_notif.message = "%s posted a new event, \"%s\"." % (group.first_name, new_event.name)
                        new_notif.sender_pk = new_event.pk
                        new_notif.save()
                for invitee in new_event.invitees.all():
                    new_notif = Notification.objects.create(user=invitee)
                    new_notif.notification_type = "Invited to event"
                    new_notif.message = "%s invited you to come to the event \"%s\"!" % (first_name, event.name)
                    new_notif.sender_pk = event.pk
                    new_notif.save()
                new_event.create_apple_ics()
                return redirect('event_detail_view', new_event.pk)
        else:
            print form.errors
            context['errors'] = form.errors
            form = EventModelCreateForm(initial=return_dict(form.data))
            form.fields['groups'].queryset = groups
            form.fields['host'].queryset = friends
            context['form'] = form
    else:
        for event in Event.objects.filter(name=None, host=request.user.profile):
            event.delete()
        pk = Event.objects.order_by('id').last().pk + 1
        event_created = Event.objects.create(public=True, pk=pk)
        event_created.host.add(request.user.profile)
        form = EventModelCreateForm(instance=event_created)
        form.fields['date_happening'].initial = timezone.now().isoformat('T')
        form.fields['time_starting'].initial = timezone.now().isoformat('T')
        form.fields['time_ending'].initial = timezone.now().isoformat('T')
        context['event_pk'] = event_created.pk

        group_pk = request.GET.get('group_pk', '')

        
        if group_pk != '':
            form.fields['groups'].queryset = groups
            form.fields['groups'].initial = [Group.objects.get(pk=group_pk), ]

        else:
            form.fields['groups'].queryset = groups


        form.fields['host'].queryset = friends

        context['form'] = form
        

    return render_to_response('event_create.html', context, context_instance=RequestContext(request))

def return_dict(dictionary):
    form_dict = {}
    for key in dictionary:
        form_dict[key] = dictionary[key]
    return form_dict


@login_required
def event_update_view(request, pk):
    context = {}
    event = Event.objects.get(pk=pk)
    if request.user.profile not in event.host.all():
        return redirect('event_list_view')

    context['event'] = event

    date_happening = event.date_happening
    time_starting = event.time_starting
    location = event.location

    form = EventModelUpdateForm(request.POST or None, instance=event)


    friends = request.user.profile.friends.all()
    groups = request.user.profile.groups_in.filter(admin_only=False)
    admin_groups = request.user.profile.groups_in.filter(admin_only=True, admin=request.user.profile)
    
    groups = groups | admin_groups    

    form.fields['host'].queryset = friends
    form.fields['groups'].queryset = groups
    context['form'] = form

    if request.method == 'POST':
        if form.is_valid():
            should_save = True
            updated_event = form.save(commit=False)
            event = datetime.combine(updated_event.date_happening, updated_event.time_starting)
            event_ending = datetime.combine(updated_event.date_happening, updated_event.time_ending)

            timezone_inst = form.data['timezone']
            if not timezone_inst:
                timezone_inst = 'UTC'
                print "UTC'd"
            event = event.replace(tzinfo=pytz.timezone(timezone_inst))
            event = event.astimezone(pytz.utc)
            event_ending = event_ending.replace(tzinfo=pytz.timezone(timezone_inst))
            event_ending = event_ending.astimezone(pytz.utc)
            if event < timezone.now():
                should_save = False
                context['errors'] = "The event date was already in the past! Try again."
                form = EventModelCreateForm(initial=return_dict(form.data))
                form.fields['groups'].queryset = groups
                form.fields['host'].queryset = friends
                context['form'] = form

            elif not updated_event.public and len(form.cleaned_data['groups']) is 0:
                should_save = False
                context['errors'] = "An event must either be public, or have at least one group to be displayed in."
                form = EventModelCreateForm(initial=return_dict(form.data))
                form.fields['host'].queryset = friends
                form.fields['groups'].queryset = groups
                context['form'] = form

            if should_save:
                updated_event.date_happening = event.date()
                updated_event.time_starting = event.time()
                updated_event.time_ending = event_ending.time()
                updated_event.save()
                form.save_m2m()
                updated_event.host.add(request.user.profile)
                for host in updated_event.host.all():
                    updated_event.people_coming.add(host)
                
                updated_event.create_apple_ics()

                changed = ""

                if location != updated_event.location:
                    changed = "location"
                if date_happening != updated_event.date_happening:
                    if "location" in changed:
                        changed += " and date"
                    else:
                        changed += "date"
                if time_starting != updated_event.time_starting:
                    if 'date' in changed or 'location' in changed:
                        if 'and' in changed:
                            changed = changed.replace(' and', ',')
                        changed += " and "
                    changed += "time"

                if changed != "":
                    for person in updated_event.people_coming.exclude(pk=request.user.profile.pk):
                        new_notif = Notification.objects.create(user=person)
                        new_notif.notification_type = "Event Updated"
                        new_notif.message = "%s changed the %s of the event %s!" % (request.user.profile.first_name, changed, updated_event.name)
                        new_notif.sender_pk = updated_event.pk
                        new_notif.save()


                if request.POST.get('_finish'):
                    return redirect('event_detail_view', pk)
                else:
                    context['saved'] = "%s saved!" % updated_event
        else:
            print form.errors
            context['errors'] = form.errors
            form = EventModelCreateForm(initial=return_dict(form.data))
            form.fields['groups'].queryset = groups
            form.fields['host'].queryset = friends
            context['form'] = form

    return render_to_response('event_update.html', context, context_instance=RequestContext(request))



@login_required
def event_delete_view(request, pk):
    event = Event.objects.get(pk=pk)

    for person in event.people_coming.exclude(pk=request.user.profile.pk):
        new_notif = Notification.objects.create(user=person)
        new_notif.notification_type = "Event Cancelled"
        new_notif.message = "%s <strong>cancelled</strong> the event %s." % (request.user.profile.first_name, event.name)
        new_notif.sender_pk = event.pk
        new_notif.save()

    event.delete()

    return redirect('event_list_view')


# Comment Views!

def comment_delete_view(request, pk):
    comment = Comment.objects.get(pk=pk)
    event_pk = comment.event.pk
    comment.delete()

    return redirect('{}#comment-section'.format(resolve_url('event_detail_view', pk=event_pk)))


# Group Views!

@login_required
def group_list_view(request):
    groups = Group.objects.filter(members=request.user.profile)

    context = {}
    context['groups'] = groups

    context['group_requests'] = request.user.profile.group_requests.all()
    context['requested_groups'] = request.user.profile.requested_groups.all()

    return render_to_response('group_list.html', context, context_instance=RequestContext(request))


@login_required
def group_member_view(request, pk):
    context = {}

    group = Group.objects.get(pk=pk)
    context['group'] = group

    is_member = request.user.profile in group.members.all()
    context['is_member'] = is_member
    context['is_admin'] = is_member and request.user.profile in group.admin.all()
    context['group_requested_by_member'] = request.user.profile in group.member_requests.all()
    context['member_requested_by_group'] = group in request.user.profile.group_requests.all()

    context['members'] = [e for e in group.members.all()]
    context['admin'] = [e for e in group.admin.filter(pk__in=group.members.values_list('pk', flat=True))]
    context['member_requests'] = [e for e in group.member_requests.all()]



    return render_to_response('group_member_view.html', context, context_instance=RequestContext(request))


@login_required
def group_event_list(request, pk):
    context = {}

    group = Group.objects.get(pk=pk)
    if request.user.profile.pk not in group.members.values_list('pk', flat=True):
        return redirect('group_member_view', pk)

    context['group'] = group

    is_member = request.user.profile in group.members.all()
    context['is_member'] = is_member
    context['is_admin'] = is_member and request.user.profile in group.admin.all()
    context['group_requested_by_member'] = request.user.profile in group.member_requests.all()
    context['member_requested_by_group'] = group in request.user.profile.group_requests.all()

    context['admin'] = [e for e in group.admin.filter(pk__in=group.members.values_list('pk', flat=True))]

    group_events = Event.objects.filter(groups=group)
    my_events = request.user.profile.events_hosted.filter(groups=group)

    order = request.GET.get('order', '')

    if order:
        context['order'] = True
        events = sorted(list(set(group_events) | set(my_events)), key=attrgetter('date_posted'), reverse=True)
    else:
        events = sorted(list(set(group_events) | set(my_events)), key=attrgetter('date_happening', 'time_starting')) #, reverse=True)

    for event in events:
        event_date = datetime.combine(date=event.date_happening, time=event.time_starting)
        
        timezone_inst = ""
        if not timezone_inst:
            timezone_inst = 'UTC'

        event_date = event_date.replace(tzinfo=pytz.timezone(timezone_inst))
        if event_date < timezone.now():
            for host in event.host.all():
                host.events_hosted.remove(event)
                host.past_events.add(event)
            event.people_coming.clear()
            event.people_not_coming.clear()
            event.people_who_posted_it.clear()
            event.people_who_shared_it.clear()
            try:
                os.remove(event.ics.file.name)
            except:
                pass
            events.remove(event)

    context['today'] = datetime.now()
    context['events'] = events
    context['my_events'] = my_events

    return render_to_response('group_event_list.html', context, context_instance=RequestContext(request))


@login_required
def group_create_view(request):

    context = {} 
    form = GroupModelCreateForm()
    friends = request.user.profile.friends.all()    
    form.fields['admin'].queryset = friends    
    context['form'] = form

    if request.method == 'POST':
        form = GroupModelCreateForm(request.POST, request.FILES)
        if form.is_valid():
            new_group = form.save(commit=False)
            new_group.save()
            form.save_m2m()
            for admin in new_group.admin.all():
                new_group.invited_people.add(admin)
            new_group.admin.add(request.user.profile)
            new_group.members.add(request.user.profile)
                
            return redirect('group_member_view', new_group.pk)
        else:
            context['errors'] = form.errors
    return render_to_response('group_create.html', context, context_instance=RequestContext(request))


@login_required
def group_update_view(request, pk):

    context = {}
    group = Group.objects.get(pk=pk)
    if request.user.profile not in group.admin.all():
        return redirect('group_list_view')
    
    context['group'] = group

    form = GroupModelUpdateForm(request.POST or None, instance=group)
    group_members = group.members.exclude(pk__in=group.admin.values_list('pk', flat=True))

    form.fields['members'].queryset = group_members
    context['form'] = form

    if request.method == 'POST':
        if form.is_valid():
            updated_group = form.save(commit=False)
            form.save_m2m()
            updated_group.members.add(request.user.profile)

            context['saved'] = '%s saved!' % updated_group.name
            updated_group.save()
            if request.POST.get('_finish'):
                return redirect('group_member_view', updated_group.pk)
        else:
            context['errors'] = form.errors

    return render_to_response('group_update.html', context, context_instance=RequestContext(request))


@login_required
def group_delete_view(request, pk):

    Group.objects.get(pk=pk).delete()

    return redirect('group_list_view')



# User / Profile Views!
@login_required
def profile_detail_view(request, pk):  
    profile = Profile.objects.get(pk=pk)

    context = {}
    context['profile'] = profile

    if request.user.is_authenticated():
        context['logged_in'] = True
        context['not_friends'] = request.user.profile not in profile.friends.all()
        context['friend_requested_by_you'] = request.user.profile in profile.friend_requests.all()
        context['friend_requested_by_them'] = profile in request.user.profile.friend_requests.all()

    if str(pk) == str(request.user.profile.pk):
        return render_to_response('your_profile_detail.html', context, context_instance=RequestContext(request))
    return render_to_response('profile_detail.html', context, context_instance=RequestContext(request))


@login_required
def friend_list(request):
    context = {}
    friends = [friend for friend in request.user.profile.friends.all()]
    context['friends'] = friends
    friend_lists = [e for e in request.user.profile.lists.all()]

    context['friend_lists'] = friend_lists

    return render_to_response('friend_list.html', context, context_instance=RequestContext(request))


@login_required
def other_friend_list(request, pk):
    context = {}
    if pk is request.user.profile.pk:
        return redirect('friend_list')
    profile = Profile.objects.get(pk=pk)
    context['profile'] = profile

    friends = [friend for friend in profile.friends.all()]
    context['friends'] = friends

    return render_to_response('other_friend_list.html', context, context_instance=RequestContext(request))


@login_required
def other_mutual_list(request, pk):
    context = {}
    if pk is request.user.profile.pk:
        return redirect('friend_list')
    profile = Profile.objects.get(pk=pk)
    context['profile'] = profile

    friends = [friend for friend in profile.friends.all()]
    mutual = set(friends) & set(request.user.profile.friends.all())
    context['mutual'] = mutual


    return render_to_response('other_mutual_list.html', context, context_instance=RequestContext(request))


@login_required
def search_profiles(request):
    profiles = []

    context = {}
    form = SearchProfile(request.POST or None)
    context['get'] = request.method == 'GET'
    if request.method == 'POST':
        if form.is_valid():
            search = form.cleaned_data.get('search', '').strip(' ')
            if " " in search:
                first, space, last = search.partition(' ')
                names = Profile.objects.filter(first_name__istartswith=first, last_name__istartswith=last)
            else:
                names = Profile.objects.filter(Q(first_name__istartswith=search) | Q(last_name__istartswith=search) )

            username = Profile.objects.filter(username__istartswith=search)
            result_list = list(set(names) | set(username))
            if request.user.profile in result_list:
                result_list.remove(request.user.profile)
            profiles = result_list

    context['profiles'] = profiles
    context['form'] = form

    return render_to_response('search_profiles.html', context, context_instance=RequestContext(request))


@login_required
def profile_create_view(request):
    new_profile, mih = Profile.objects.get_or_create(user=request.user)
    new_profile.username = new_profile.user.username
    new_profile.first_name = new_profile.user.first_name
    new_profile.last_name = new_profile.user.last_name

    new_profile.save()
    print 'lol'

    return redirect('event_list_view')


@login_required
def profile_update_view(request, pk):

    context = {}

    profile = Profile.objects.get(pk=pk)

    context['profile'] = profile

    form = ProfileModelUpdateForm(request.POST or None, instance=profile)

    context['form'] = form

    if request.method == 'POST':
        form = ProfileModelUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            context['saved'] = 'Your profile has been saved!'

            if request.POST.get('_finish'):
                return redirect('profile_detail_view', pk)
        else:
            context['errors'] = form.errors

    return render_to_response('profile_update.html', context, context_instance=RequestContext(request))



@login_required
def profile_delete_view(request, pk):

    Profile.objects.get(pk=pk).delete()

    return redirect('profile_list_view')


# Permission Views!


@login_required
def logout_view(request):

    logout(request)

    return redirect('new_user')


def new_user(request):    
    context = {}

    if request.user.is_authenticated():
        return redirect('event_list_view')

    context['next'] = request.GET.get('next', None)


    # form = UserLogin(request.POST or None)
    # context['form'] = form

    # if request.method == "POST":
    #     if form.is_valid():

    #         username = form.cleaned_data['username']
    #         password = form.cleaned_data['password']

    #         auth_user = authenticate(username=username, password=password)

    #         if auth_user is not None:
    #             if auth_user.is_active:
    #                 login(request, auth_user)
    #                 context['valid'] = "Login Successful"

    #                 return redirect('event_list_view')
    #             else:
    #                 context['valid'] = "Invalid User"
    #         else:
    #             context['valid'] = "Login Failed! Try again"
    return render_to_response('new_user.html', context, context_instance=RequestContext(request))

@login_required
def full_notifications(request):
    context = {}
    context['profile'] = request.user.profile
    context['friend_requests'] = request.user.profile.friend_requests.all()
    context['group_requests'] = request.user.profile.group_requests.all()

    return render_to_response('full_notifications.html', context, context_instance=RequestContext(request))



def about_view(request):
    if request.user.is_authenticated():
        request.user.profile.new_user = False
        request.user.profile.save()
    return render(request, 'about.html')



def thank_you(request):
    return render(request, 'thanks.html')


def contact_view(request):
    context = {}
    form = ContactForm(request.POST or None)
    context['form'] = form

    if request.method == "POST":
        if form.is_valid():
            author = form.cleaned_data['author']
            email = form.cleaned_data['email']
            comment = form.cleaned_data['comment']

            print author, email, comment
            send_mail("Social Media you're building: %s" % author, comment, email, [settings.EMAIL_HOST_USER], fail_silently=False)
            return redirect('thank_you')
        else:
            context['errors'] = form.errors


    return render_to_response('contact.html', context, context_instance=RequestContext(request))


# friendlist views

@login_required
def friend_list(request):
    context = {}
    friends = [friend for friend in request.user.profile.friends.all()]
    context['friends'] = friends
    friend_lists = [e for e in request.user.profile.lists.all().order_by('name')]

    context['friend_lists'] = friend_lists

    form = FriendListCreate(request.POST or None)
    context['form'] = form

    if request.method == "POST":
        if form.is_valid():
            name = form.cleaned_data['name'].strip()
            if name != "" and name is not None:
                new_friend_list, created = FriendList.objects.get_or_create(owner=request.user.profile, name=name)
                if created:
                    return redirect('friend_list_detail_view', new_friend_list.pk)
                else:
                    context['errors'] = "You already have a friend list named \"%s\"! Try creating a different list." % name

    return render_to_response('friend_list.html', context, context_instance=RequestContext(request))

@login_required
def friend_list_detail_view(request, pk):
    friend_list = FriendList.objects.get(pk=pk)
    if request.user.profile != friend_list.owner:
        return redirect('friend_list_list_view')

    context = {}

    friends = [friend for friend in friend_list.people.all()]
    context['friends'] = friends
    friend_lists = [e for e in request.user.profile.lists.all().order_by('name')]

    context['friend_lists'] = friend_lists
    context['friend_list'] = friend_list


    form = FriendListCreate(request.POST or None)
    context['form'] = form

    if request.method == "POST":
        if form.is_valid():
            name = form.cleaned_data['name'].strip()
            if name != "" and name is not None:
                new_friend_list, created = FriendList.objects.get_or_create(owner=request.user.profile, name=name)
                if created:
                    return redirect('friend_list_detail_view', new_friend_list.pk)
                else:
                    context['errors'] = "You already have a friend list named \"%s\"! Try creating a different list." % name

    return render_to_response('friend_list_detail.html', context, context_instance=RequestContext(request))


@login_required
def pick_friends_for_list(request, pk):

    context = {}

    friend_list = FriendList.objects.get(pk=pk)

    context['friend_list'] = friend_list
    context['friends'] = request.user.profile.friends.exclude(pk__in=friend_list.people.values_list('pk', flat=True))


    return render_to_response('pick_friends_for_list.html', context, context_instance=RequestContext(request))


@login_required
def invite_friends_to_event_view(request, pk):
    context = {}
    event = Event.objects.get(pk=pk)
    context['event'] = event

    friends = request.user.profile.friends.exclude(events_going_to=event)

    context['friends'] = friends

    friend_lists = request.user.profile.lists.all()

    context['friend_lists'] = friend_lists

    return render_to_response('invite_friends_to_event.html', context, context_instance=RequestContext(request))



@login_required
def invite_friend_lists_to_event_view(request, pk):
    context = {}
    event = Event.objects.get(pk=pk)
    context['event'] = event

    friend_lists = request.user.profile.lists.all()

    context['friend_lists'] = friend_lists

    return render_to_response('invite_friend_lists_to_event.html', context, context_instance=RequestContext(request))


@login_required
def friend_list_delete_view(request, pk):

    FriendList.objects.get(pk=pk).delete()

    return redirect('friend_list')


# ajax views

@login_required
def accept_request(request):
    pk = request.GET.get('pk')
    prof = Profile.objects.get(pk=pk)

    new_notif = Notification.objects.create()
    new_notif.user = prof
    new_notif.notification_type = "Friend Request"
    new_notif.message = "%s accepted your friend request!" % request.user.profile.first_name
    new_notif.sender_pk = request.user.profile.pk
    new_notif.save()

    prof.friends.add(request.user.profile)
    request.user.profile.friends.add(prof)

    request.user.profile.friend_requests.remove(prof)

    prof_list = []

    prof_list.append(prof.user.first_name)
    prof_list.append(request.user.profile.friend_requests.count())

    return JsonResponse(prof_list, safe=False)


@login_required
def reject_request(request):
    pk = request.GET.get('pk')
    prof = Profile.objects.get(pk=pk)
    print prof

    request.user.profile.friend_requests.remove(prof)

    prof_list = []

    prof_list.append(prof.user.first_name)
    prof_list.append(request.user.profile.friend_requests.count())

    return JsonResponse(prof_list, safe=False)


@login_required
def request_friendship(request):
    pk = request.GET.get('pk')
    prof = Profile.objects.get(pk=pk)
    print prof
    prof.friend_requests.add(request.user.profile)
    prof_list = []

    prof_list.append(prof.user.first_name)

    return JsonResponse(prof_list, safe=False)


@login_required
def cancel_request(request):
    pk = request.GET.get('pk')
    prof = Profile.objects.get(pk=pk)
    print prof
    prof.friend_requests.remove(request.user.profile)
    prof_list = []

    prof_list.append(prof.user.first_name)

    return JsonResponse(prof_list, safe=False)



@login_required
def delete_friendship(request):
    pk = request.GET.get('pk')
    prof = Profile.objects.get(pk=pk)
    print prof
    prof.friends.remove(request.user.profile)
    prof.followers.remove(request.user.profile)
    request.user.profile.friends.remove(prof)
    request.user.profile.followers.remove(prof)
    prof_list = []

    prof_list.append(prof.user.first_name)

    return JsonResponse(prof_list, safe=False)



@login_required
def request_membership_in_group(request):
    pk = request.GET.get('pk')
    group = Group.objects.get(pk=pk)
    print group
    group.member_requests.add(request.user.profile)
    group_list = []

    group_list.append(group.name)

    member_ids = group.members.all().values_list('pk', flat=True)

    for admin in group.admin.filter(pk__in=member_ids):
        new_notif = Notification.objects.create(notification_type='Group Request')
        new_notif.user = admin
        new_notif.message = "%s has requested to join your group %s." % (request.user.profile.first_name, group.name)
        new_notif.sender_pk = group.pk
        new_notif.save()

    return JsonResponse(group_list, safe=False)


@login_required
def cancel_request_membership_in_group(request):
    pk = request.GET.get('pk')
    group = Group.objects.get(pk=pk)
    print group
    group.member_requests.remove(request.user.profile)
    group_list = []

    group_list.append(group.name)

    return JsonResponse(group_list, safe=False)


@login_required
def invite_friend_to_group(request):
    person_pk = request.GET.get('person_pk')
    group_pk = request.GET.get('group_pk')

    friend = Profile.objects.get(pk=person_pk)
    group = Group.objects.get(pk=group_pk)

    friend.group_requests.add(group)

    group_list = []
    group_list.append(group.name)

    return JsonResponse(group_list, safe=False)



@login_required
def cancel_invite_friend_to_group(request):
    person_pk = request.GET.get('person_pk')
    group_pk = request.GET.get('group_pk')

    friend = Profile.objects.get(pk=person_pk)
    group = Group.objects.get(pk=group_pk)

    friend.group_requests.remove(group)

    group_list = []
    group_list.append(group.name)

    return JsonResponse(group_list, safe=False)



@login_required
def reject_invitation_from_group(request):
    person_pk = request.GET.get('person_pk')
    group_pk = request.GET.get('group_pk')

    friend = Profile.objects.get(pk=person_pk)
    group = Group.objects.get(pk=group_pk)

    friend.group_requests.remove(group)
    group.member_requests.remove(friend)

    group_list = []
    group_list.append(group.name)
    group_list.append(friend.first_name)
    group_list.append(friend.group_requests.count())

    return JsonResponse(group_list, safe=False)


@login_required
def user_accepts_invitation(request):
    group_pk = request.GET.get('group_pk')
    group = Group.objects.get(pk=group_pk)
    member_ids = group.members.all().values_list('pk', flat=True)

    for admin in group.admin.filter(pk__in=member_ids):
        new_notif = Notification.objects.create(notification_type='Group Invitation')
        new_notif.user = admin
        new_notif.message = "%s accepted the invitation to join %s!" % (request.user.profile.first_name, group.name)
        new_notif.sender_pk = group.pk
        new_notif.save()

    group.members.add(request.user.profile)
    request.user.profile.group_requests.remove(group)
    group.member_requests.remove(request.user.profile)

    group_list = []
    group_list.append(group.name)
    group_list.append(request.user.profile.first_name)
    group_list.append(request.user.profile.group_requests.count())    

    return JsonResponse(group_list, safe=False)


@login_required
def group_approves_request(request):
    person_pk = request.GET.get('person_pk')
    group_pk = request.GET.get('group_pk')

    friend = Profile.objects.get(pk=person_pk)
    group = Group.objects.get(pk=group_pk)

    group.members.add(friend)
    friend.group_requests.remove(group)
    group.member_requests.remove(friend)

    group_list = []
    group_list.append(group.name)
    group_list.append(friend.first_name)

    new_notif = Notification.objects.create(notification_type='Group Request')
    new_notif.user = friend
    new_notif.message = "%s accepted your request to join!" % group.name
    new_notif.sender_pk = group.pk
    new_notif.save()

    return JsonResponse(group_list, safe=False)


@login_required
def leave_group(request):
    pk = request.GET.get('pk')
    group = Group.objects.get(pk=pk)
    print group
    group.members.remove(request.user.profile)
    group.admin.remove(request.user.profile)
    group.followers.remove(request.user.profile)

    group_list = []
    group_list.append(group.name)

    return JsonResponse(group_list, safe=False)


@login_required
def can_come(request):
    pk = request.GET.get('pk', '')
    event = Event.objects.get(pk=pk)
    event.people_not_coming.remove(request.user.profile)
    event.people_coming.add(request.user.profile)

    hosts = ""
    host_list = [e for e in event.host.all()]
    for count, e in enumerate(host_list):
        if e.notifications.filter(read=False, sender_pk=event.pk, notification_type__istartswith='Confirm can come').exists():
            notif = e.notifications.get(read=False, sender_pk=event.pk, notification_type__istartswith='Confirm can come')
            
            notif.message = "%d people are now coming to your event %s." % (event.people_coming.count(), event.name)
            notif.date_posted = datetime.now()
            notif.save()
        else:
            new_notif = Notification.objects.create(user=e)
            new_notif.notification_type = "Confirm can come to event"
            new_notif.message = '%s is coming to "%s", the event you\'re hosting.' % (request.user.profile.first_name, event.name)
            new_notif.sender_pk = event.pk
            new_notif.save()
        if count >= len(host_list)-1:
            hosts += "%s" % e
        else:
            hosts += "%s, " % e
    event_date = datetime.combine(event.date_happening, event.time_starting)
    date = "%s" % event_date.isoformat('T')
    posted = "%s" % event.date_posted.isoformat(' ')
    return JsonResponse([event.name, hosts, date, "People coming: %d" % event.people_coming.count(), host_list[0].picture.url, posted, event.description, "People not coming: %d" % event.people_not_coming.count()], safe=False)


@login_required
def cannot_come(request):
    pk = request.GET.get('pk', '')
    event = Event.objects.get(pk=pk)
    event.people_coming.remove(request.user.profile)
    event.invitees.remove(request.user.profile)
    event.people_not_coming.add(request.user.profile)
    hosts = ""
    host_list = [e for e in event.host.all()]
    for count, e in enumerate(host_list):
        if count >= len(host_list)-1:
            hosts += "%s" % e.first_name
        else:
            hosts += "%s, " % e.first_name
    event_date = datetime.combine(event.date_happening, event.time_starting)
    date = "%s" % event_date.isoformat('T')    
    return JsonResponse([event.name, hosts, date, event.people_coming.count(), host_list[0].picture.url], safe=False)


@login_required
def cancel_decision(request):
    pk = request.GET.get('pk', '')
    event = Event.objects.get(pk=pk)
    event.people_coming.remove(request.user.profile)
    event.people_not_coming.remove(request.user.profile)
    hosts = ""
    host_list = [e for e in event.host.all()]
    for count, e in enumerate(host_list):
        if e.notifications.filter(read=False, sender_pk=event.pk, notification_type__istartswith='Confirm can come').exists():
            notif = e.notifications.get(read=False, sender_pk=event.pk, notification_type__istartswith='Confirm can come')
            
            notif.message = "%d people are now coming to your event %s." % (event.people_coming.count(), event.name)
            notif.date_posted = datetime.now()
            notif.save()
        else:
            new_notif = Notification.objects.create(user=e)
            new_notif.notification_type = "Confirm can come to event"
            new_notif.message = "%d people are now coming to your event %s." % (event.people_coming.count(), event.name)
            new_notif.sender_pk = event.pk
            new_notif.save()
        if count >= len(host_list)-1:
            hosts += "%s" % e
        else:
            hosts += "%s, " % e
    event_date = datetime.combine(event.date_happening, event.time_starting)
    date = "%s" % event_date.isoformat('T')
    posted = "%s" % event.date_posted.isoformat(' ')
    return JsonResponse([event.name, hosts, date, event.people_coming.count(), host_list[0].picture.url, posted, event.description], safe=False)


@login_required
def clear_notification(request):
    pk = request.GET.get('pk', '')
    notif = Notification.objects.get(pk=pk)
    notif.read = True
    notif.save()
    return JsonResponse([request.user.profile.unread_notifications().count(),], safe=False)


@login_required
def ajax_friends(request):
    context = {}
    pk = request.GET.get('group_pk')
    group = Group.objects.get(pk=pk)
    context['group'] = group
    member_ids = group.members.all().values_list('pk', flat=True)
    friends = request.user.profile.friends.exclude(pk__in=member_ids)
    context['friends'] = friends

    friend_lists = request.user.profile.lists.all()
    context['friend_lists'] = friend_lists

    return render_to_response('friend_invite.html', context, context_instance=RequestContext(request))


@login_required
def ajax_facebook_friends(request):
    context = {}

    social = request.user.social_auth.get(provider='facebook')
    response = requests.get('https://graph.facebook.com/v2.5/{0}/friends'.format(social.uid),params={'access_token': social.extra_data['access_token']})
    json = response.json()
    friends = json.get('data')
    friend_list = []
    for friend in friends:
        friend_list.append(friend.get('id'))

    friends = Profile.objects.filter(user__social_auth__uid__in=friend_list)
    friends = friends.exclude(pk__in=request.user.profile.friends.values_list('pk', flat=True))
    context['friends'] = friends

    return render_to_response('facebook_friends.html', context, context_instance=RequestContext(request))

@login_required
def share_event(request):
    pk = request.GET.get('pk', '')
    event = Event.objects.get(pk=pk)

    if event not in request.user.profile.events_posted.all():
        request.user.profile.events_posted.add(event)
        request.user.profile.shared_events.add(event)
        added = True
        for follower in request.user.profile.followers.all():
            if follower not in event.host.all():
                if not follower.notifications.filter(read=False, sender_pk=event.pk, notification_type__iendswith=request.user.profile.pk).exists():
                    new_notif = Notification.objects.create(user=follower)
                    new_notif.notification_type = "Following shared event %s" % request.user.profile.pk
                    new_notif.message = "%s shared a new event, \"%s\"." % (request.user.profile.first_name, event.name)
                    new_notif.sender_pk = event.pk
                    new_notif.save()

        for host in event.host.all():
            if not host.notifications.filter(read=False, sender_pk=event.pk, notification_type__iendswith=request.user.profile.pk).exists():
                new_notif = Notification.objects.create(user=host)
                new_notif.notification_type = "Shared your event %s" % request.user.profile.pk
                new_notif.message = '%s shared your event "%s".' % (request.user.profile.first_name, event.name)
                new_notif.sender_pk = event.pk
                new_notif.save()
    else:
        request.user.profile.events_posted.remove(event)
        request.user.profile.shared_events.remove(event)
        added = False
    
    return JsonResponse([event.name, added], safe=False)


@login_required
def subscribe(request, pk):
    profile = Profile.objects.get(pk=pk)
    
    if request.user.profile.pk not in profile.followers.values_list('pk', flat=True):
        profile.followers.add(request.user.profile)
    else:
        profile.followers.remove(request.user.profile)

    return redirect('profile_detail_view', pk)


@login_required
def subscribe_group(request, pk):
    group = Group.objects.get(pk=pk)
    
    if request.user.profile.pk not in group.followers.values_list('pk', flat=True):
        group.followers.add(request.user.profile)
    else:
        group.followers.remove(request.user.profile)

    return redirect('group_event_list', pk)


@login_required
def add_friend_to_friend_list(request):
    friend_pk = request.GET.get('friend_pk')
    list_pk = request.GET.get('list_pk')

    friend = Profile.objects.get(pk=friend_pk)
    friend_list = FriendList.objects.get(pk=list_pk)

    friend_list.people.add(friend)

    return JsonResponse({'success': True})


@login_required
def invite_friend_to_event(request):
    friend_pk = request.GET.get('friend_pk')
    event_pk = request.GET.get('event_pk')
    event = Event.objects.get(pk=event_pk)

    extend_event_invite(request.user.profile.first_name, friend_pk, event)

    return JsonResponse({'success': True})


@login_required
def invite_friend_list_to_event(request):
    friend_list_pk = request.GET.get('friend_list_pk')
    event_pk = request.GET.get('event_pk')
    event = Event.objects.get(pk=event_pk)
    friend_list = FriendList.objects.get(pk=friend_list_pk)

    for friend_pk in friend_list.people.values_list('pk', flat=True):
        if friend_pk not in event.people_coming.values_list('pk', flat=True):
            extend_event_invite(request.user.profile.first_name, friend_pk, event)

    return JsonResponse({'success': True})


def extend_event_invite(first_name, friend_pk, event):
    friend = Profile.objects.get(pk=friend_pk)

    if event.name:
        if friend not in event.invitees.all():
            new_notif = Notification.objects.create(user=friend)
            new_notif.notification_type = "Invited to event"
            new_notif.message = "%s invited you to come to the event \"%s\"!" % (first_name, event.name)
            new_notif.sender_pk = event.pk
            new_notif.save()

    event.invitees.add(friend)

@login_required
def share_buttons(request, pk):
    context = {}
    event = Event.objects.get(pk=pk)
    context['event'] = event


    context['share_url'] = 'https://www.facebook.com/dialog/feed?app_id={0}&display=popup&name={2}&description={3}&caption=WAYD%20events&link={1}&redirect_uri=http://social.coleclayman.us'.format(FB_APP_ID, urllib.quote_plus("http://127.0.0.1:8000%s" % resolve_url('event_detail_view', pk=pk)), 'Check out "%s" on WAYD Events!' % event.name, event.description)

    return render_to_response('share_buttons.html', context, context_instance=RequestContext(request))


@login_required
def calendar_buttons(request, pk):
    context = {}

    event = Event.objects.get(pk=pk)
    context['event'] = event

    url_date_starting = datetime.combine(date=event.date_happening, time=event.time_starting).isoformat().replace('-', '').replace(':', '')
    url_date_ending = datetime.combine(date=event.date_happening, time=event.time_ending).isoformat().replace('-', '').replace(':', '')
    context['google_cal'] = "https://www.google.com/calendar/render?action=TEMPLATE&text={0}&dates={1}/{2}&details=For+details,+link+here%3a+http://www.example.com&location={3}&sf=true&output=xml".format(event.name, url_date_starting, url_date_ending, event.location)


    context['apple_cal'] = "http://social.coleclayman.us%s" % event.ics.url

    return render_to_response('calendar_buttons.html', context, context_instance=RequestContext(request))


@login_required
def mark_non_new_user(request):
    request.user.profile.new_user = False
    request.user.profile.save()


@login_required
def search_invite_event_json(request, pk):
    _dict = {}
    search = request.GET.get('search')

    friend_list = []
    friendlist_list = []
    _dict['friends'] = friend_list
    _dict['friend_lists'] = friendlist_list

    event = Event.objects.get(pk=pk)
    if search.strip():
        if " " in search:
            first, space, last = search.partition(' ')
            friends = request.user.profile.friends.exclude(events_going_to=event).filter(first_name__istartswith=first, last_name__icontains=last)
        else:
            friends = request.user.profile.friends.exclude(events_going_to=event).filter(Q(first_name__istartswith=search) | Q(last_name__istartswith=search) | Q(username__istartswith=search))
        friend_lists = request.user.profile.lists.filter(name__istartswith=search)
    else:
        friends = request.user.profile.friends.exclude(events_going_to=event)
        friend_lists = request.user.profile.lists.all()


    for friend in friends:
        im = get_thumbnail(friend.picture, '200x200', crop='center', quality=99)
        friend_list.append({'name': '%s %s' % (friend.first_name, friend.last_name),
                                'pk': friend.pk,
                                'img_url': im.url,
                                'invited': friend.pk in event.invitees.values_list('pk', flat=True)})
    if len(friend_list) is 0:
        _dict['no_friends'] = True

    for friendlist in friend_lists:
        friendlist_list.append({'name': friendlist.name,
                                'pk': friendlist.pk})

    if len(friendlist_list) is 0:
        _dict['no_friend_lists'] = True

    return JsonResponse(_dict)


@login_required
def search_invite_group_json(request, pk):
    _dict = {}
    search = request.GET.get('search')

    friend_list = []
    friendlist_list = []
    _dict['friends'] = friend_list
    _dict['friend_lists'] = friendlist_list

    group = Group.objects.get(pk=pk)
    if search.strip():
        if " " in search:
            first, space, last = search.partition(' ')
            friends = request.user.profile.friends.exclude(groups_in=group).filter(first_name__istartswith=first, last_name__icontains=last)
        else:
            friends = request.user.profile.friends.exclude(groups_in=group).filter(Q(first_name__istartswith=search) | Q(last_name__istartswith=search) | Q(username__istartswith=search))
        friend_lists = request.user.profile.lists.filter(name__istartswith=search)
    else:
        friends = request.user.profile.friends.exclude(groups_in=group)
        friend_lists = request.user.profile.lists.all()


    for friend in friends:
        im = get_thumbnail(friend.picture, '200x200', crop='center', quality=99)
        friend_list.append({'name': '%s %s' % (friend.first_name, friend.last_name),
                                'pk': friend.pk,
                                'img_url': im.url,
                                'invited': friend.pk in group.invited_people.values_list('pk', flat=True)})
    if len(friend_list) is 0:
        _dict['no_friends'] = True

    for friendlist in friend_lists:
        friendlist_list.append({'name': friendlist.name,
                                'pk': friendlist.pk})

    if len(friendlist_list) is 0:
        _dict['no_friend_lists'] = True

    return JsonResponse(_dict)

def slugify(string):
    return string.lower().replace(' ', '-')
