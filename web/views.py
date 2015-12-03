import pytz
from operator import attrgetter
from datetime import datetime

from django.shortcuts import render, render_to_response, redirect
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


from main.models import Event, Group, Profile, Comment, Notification
from main.forms import SearchProfile, EventModelCreateForm, EventModelUpdateForm, GroupModelCreateForm, GroupModelUpdateForm, UserLogin, ProfileModelCreateForm, ProfileModelUpdateForm, GroupModelCreateForm, GroupModelUpdateForm, ContactForm, CommentForm



#  Event Views!

@login_required
def event_detail_view(request, pk):  
    event = Event.objects.get(pk=pk)

    context = {}
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

                new_comment.save()
                return redirect('event_detail_view', pk)

    return render_to_response('event_detail.html', context, context_instance=RequestContext(request))

@login_required
def event_list_view(request):
    if not request.user.is_authenticated():
        return redirect('new_user')

    context = {}
    order = request.GET.get('order', '')

    friend_events = Event.objects.filter(Q(host=request.user.profile.friends.all(), public=True) | Q(groups=request.user.profile.groups_in.all()) | Q(people_who_shared=request.user.profile.friends.all()))
    my_events = request.user.profile.events_hosted.all()

    if order:
        context['order'] = True
        events = sorted(list(set(friend_events) | set(my_events)), key=attrgetter('date_posted'), reverse=True)
    else:
        events = sorted(list(set(friend_events) | set(my_events)), key=attrgetter('date_happening', 'time_starting')) #, reverse=True)

    for event in events:
        event_date = datetime.combine(date=event.date_happening, time=event.time_starting)
        timezone_inst = request.session.get('django_timezone')
        if not timezone_inst:
            timezone_inst = 'UTC'

        event_date = event_date.replace(tzinfo=pytz.timezone(timezone_inst))
        if event_date < timezone.now():
            for host in event.host.all():
                host.events_hosted.remove(event)
                host.past_events.add(event)
            events.remove(event)

    context['today'] = datetime.now()
    context['events'] = events
    context['my_events'] = my_events

    return render_to_response('event_list.html', context, context_instance=RequestContext(request))
    

@login_required
def event_create_view(request):

    context = {} 
    form = EventModelCreateForm()
    friends = request.user.profile.friends.all()
    groups = request.user.profile.groups_in.all()

    form.fields['host'].queryset = friends
    form.fields['groups'].queryset = groups

    context['form'] = form
    if request.method == 'POST':
        form = EventModelCreateForm(request.POST, request.FILES)
        if form.is_valid():
            should_save = True
            new_event = form.save(commit=False)
            event = datetime.combine(new_event.date_happening, new_event.time_starting)
            timezone_inst = request.session.get('django_timezone')
            if not timezone_inst:
                timezone_inst = 'UTC'
                print "UTC'd"
            event = event.replace(tzinfo=pytz.timezone(timezone_inst))

            print timezone.localtime(event)
            if event < timezone.now():
                should_save = False
                context['errors'] = "The event date was already in the past! Try again."
                form = EventModelCreateForm(initial=return_dict(form.data))
                form.fields['groups'].queryset = groups
                form.fields['host'].queryset = friends
                context['form'] = form

            elif not new_event.public and len(form.cleaned_data['groups']) is 0:
                should_save = False
                context['errors'] = "An event must either be public, or have at least one group to be displayed in."
                form = EventModelCreateForm(initial=return_dict(form.data))
                form.fields['host'].queryset = friends
                form.fields['groups'].queryset = groups
                context['form'] = form

            if should_save:
                new_event.save()
                form.save_m2m()
                new_event.host.add(request.user.profile)
                for host in new_event.host.all():
                    new_event.people_coming.add(host)
                return redirect('event_detail_view', new_event.pk)
        else:
            print form.errors
            context['errors'] = form.errors
            form = EventModelCreateForm(initial=return_dict(form.data))
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

    form = EventModelUpdateForm(request.POST or None, instance=event)
    print form.fields['time_starting'].initial
    form.fields['time_starting'].initial = event.time_starting
    form.fields['time_ending'].initial = event.time_ending
    print form.fields['time_starting'].initial
    print form.fields['time_ending'].initial


    friends = request.user.profile.friends.all()
    groups = request.user.profile.groups_in.all()

    form.fields['host'].queryset = friends
    form.fields['groups'].queryset = groups
    context['form'] = form

    if request.method == 'POST':
        if form.is_valid():
            should_save = True
            new_event = form.save(commit=False)
            event = datetime.combine(new_event.date_happening, new_event.time_starting)
            timezone_inst = request.session.get('django_timezone')
            if not timezone_inst:
                timezone_inst = 'UTC'
                print "UTC'd"
            event = event.replace(tzinfo=pytz.timezone(timezone_inst))
            print event
            print timezone.now()
            if event < timezone.now():
                should_save = False
                context['errors'] = "The event date was already in the past! Try again."
                form = EventModelCreateForm(initial=return_dict(form.data))
                form.fields['groups'].queryset = groups
                form.fields['host'].queryset = friends
                context['form'] = form

            elif not new_event.public and len(form.cleaned_data['groups']) is 0:
                should_save = False
                context['errors'] = "An event must either be public, or have at least one group to be displayed in."
                form = EventModelCreateForm(initial=return_dict(form.data))
                form.fields['host'].queryset = friends
                form.fields['groups'].queryset = groups
                context['form'] = form

            if should_save:
                new_event.save()
                form.save_m2m()
                new_event.host.add(request.user.profile)
                for host in new_event.host.all():
                    new_event.people_coming.add(host)
                if request.POST.get('_finish'):
                    return redirect('event_detail_view', pk)

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

    Event.objects.get(pk=pk).delete()

    return redirect('event_list_view')


# Comment Views!

def comment_delete_view(request, pk):
    comment = Comment.objects.get(pk=pk)
    event_pk = comment.event.pk
    comment.delete()

    return redirect('event_detail_view', event_pk)


# Group Views!

def group_detail_view(request, slug):  
    context = {}

    name = slug.replace('-', ' ')
    group = Group.objects.get(name__iexact=name)
    context['group'] = group


    if request.user.is_authenticated():
        context['logged_in'] = True
        context['is_member'] = request.user.profile in group.members.all()
        context['is_admin'] = request.user.profile in group.admin.all()
        context['group_requested_by_member'] = request.user.profile in group.member_requests.all()
        context['member_requested_by_group'] = group in request.user.profile.group_requests.all()

    return render_to_response('group_detail.html', context, context_instance=RequestContext(request))


@login_required
def group_list_view(request):
    groups = Group.objects.filter(members=request.user.profile)

    context = {}
    context['groups'] = groups

    context['group_requests'] = request.user.profile.group_requests.all()
    context['requested_groups'] = request.user.profile.requested_groups.all()

    return render_to_response('group_list.html', context, context_instance=RequestContext(request))


@login_required
def group_event_list(request, slug):
    context = {}
    name = slug.replace('-', ' ')
    group = Group.objects.get(name__iexact=name)
    context['group'] = group
    if request.user.profile not in group.members.all():
        return redirect('group_detail_view', slugify(group.name))
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
        timezone_inst = request.session.get('django_timezone')
        if not timezone_inst:
            timezone_inst = 'UTC'

        event_date = event_date.replace(tzinfo=pytz.timezone(timezone_inst))
        if event_date < timezone.now():
            for host in event.host.all():
                host.events_hosted.remove(event)
                host.past_events.add(event)
            event.people_who_shared.clear()
            events.remove(event)

    context['today'] = timezone.now()
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
                
            return redirect('group_list_view')
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
    group_members = group.members.exclude(pk=request.user.profile.pk)

    form.fields['members'].queryset = group_members
    form.fields['admin'].queryset = group_members
    context['form'] = form

    if request.method == 'POST':
        form = GroupModelUpdateForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            new_group = form.save(commit=False)
            new_group.save()
            for admin in new_group.admin.all():
                new_group.invited_people.add(admin)
            form.save_m2m()
            new_group.admin.add(request.user.profile)
            new_group.members.add(request.user.profile)

            context['saved'] = '%s saved!' % new_group.name

            if request.POST.get('_finish'):
                return redirect('group_detail_view', slugify(new_group.name))
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


    return render_to_response('profile_detail.html', context, context_instance=RequestContext(request))


def friend_list(request):
    context = {}
    context['friends'] = request.user.profile.friends.all()

    return render_to_response('friend_list.html', context, context_instance=RequestContext(request))


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
def profile_list_view(request):

    profiles = Profile.objects.all()
    if request.user.is_authenticated():
        profiles = profiles.exclude(user=request.user)

    context = {}
    context['profiles'] = profiles

    return render_to_response('profile_list.html', context, context_instance=RequestContext(request))


@login_required
def profile_create_view(request):
    new_profile, mih = Profile.objects.get_or_create(user=request.user)
    new_profile.username = new_profile.user.username
    new_profile.first_name = new_profile.user.first_name
    new_profile.last_name = new_profile.user.last_name

    new_profile.save()

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


    form = UserLogin(request.POST or None)
    context['form'] = form

    if request.method == "POST":
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)

            if auth_user is not None:
                if auth_user.is_active:
                    login(request, auth_user)
                    context['valid'] = "Login Successful"

                    return redirect('event_list_view')
                else:
                    context['valid'] = "Invalid User"
            else:
                context['valid'] = "Login Failed! Try again"
    return render_to_response('new_user.html', context, context_instance=RequestContext(request))


def full_notifications(request):
    context = {}
    context['profile'] = request.user.profile
    context['friend_requests'] = request.user.profile.friend_requests.all()
    context['group_requests'] = request.user.profile.group_requests.all()

    return render_to_response('full_notifications.html', context, context_instance=RequestContext(request))


def about_view(request):
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


# ajax views
def accept_request(request):
    pk = request.GET.get('pk')
    prof = Profile.objects.get(pk=pk)

    new_notif = Notification.objects.create()
    new_notif.user = prof
    new_notif.notification_type = "Friend Request"
    new_notif.message = "<strong>%s</strong> accepted your friend request!" % request.user.profile.first_name
    new_notif.sender_pk = request.user.profile.pk
    new_notif.save()

    prof.friends.add(request.user.profile)
    request.user.profile.friends.add(prof)

    request.user.profile.friend_requests.remove(prof)

    prof_list = []

    prof_list.append(prof.user.first_name)
    prof_list.append(request.user.profile.friend_requests.count())

    return JsonResponse(prof_list, safe=False)


def reject_request(request):
    pk = request.GET.get('pk')
    prof = Profile.objects.get(pk=pk)
    print prof

    request.user.profile.friend_requests.remove(prof)

    prof_list = []

    prof_list.append(prof.user.first_name)
    prof_list.append(request.user.profile.friend_requests.count())

    return JsonResponse(prof_list, safe=False)


def request_friendship(request):
    pk = request.GET.get('pk')
    prof = Profile.objects.get(pk=pk)
    print prof
    prof.friend_requests.add(request.user.profile)
    prof_list = []

    prof_list.append(prof.user.first_name)

    return JsonResponse(prof_list, safe=False)


def cancel_request(request):
    pk = request.GET.get('pk')
    prof = Profile.objects.get(pk=pk)
    print prof
    prof.friend_requests.remove(request.user.profile)
    prof_list = []

    prof_list.append(prof.user.first_name)

    return JsonResponse(prof_list, safe=False)



def delete_friendship(request):
    pk = request.GET.get('pk')
    prof = Profile.objects.get(pk=pk)
    print prof
    prof.friends.remove(request.user.profile)
    request.user.profile.friends.remove(prof)
    prof_list = []

    prof_list.append(prof.user.first_name)

    return JsonResponse(prof_list, safe=False)



def request_membership_in_group(request):
    pk = request.GET.get('pk')
    group = Group.objects.get(pk=pk)
    print group
    group.member_requests.add(request.user.profile)
    group_list = []

    group_list.append(group.name)

    return JsonResponse(group_list, safe=False)


def cancel_request_membership_in_group(request):
    pk = request.GET.get('pk')
    group = Group.objects.get(pk=pk)
    print group
    group.member_requests.remove(request.user.profile)
    group_list = []

    group_list.append(group.name)

    return JsonResponse(group_list, safe=False)


def invite_friend_to_group(request):
    person_pk = request.GET.get('person_pk')
    group_pk = request.GET.get('group_pk')

    friend = Profile.objects.get(pk=person_pk)
    group = Group.objects.get(pk=group_pk)

    friend.group_requests.add(group)

    group_list = []
    group_list.append(group.name)

    return JsonResponse(group_list, safe=False)


def cancel_invite_friend_to_group(request):
    person_pk = request.GET.get('person_pk')
    group_pk = request.GET.get('group_pk')

    friend = Profile.objects.get(pk=person_pk)
    group = Group.objects.get(pk=group_pk)

    friend.group_requests.remove(group)

    group_list = []
    group_list.append(group.name)

    return JsonResponse(group_list, safe=False)


def reject_invitation_from_group(request):
    person_pk = request.GET.get('person_pk')
    group_pk = request.GET.get('group_pk')

    friend = Profile.objects.get(pk=person_pk)
    group = Group.objects.get(pk=group_pk)

    friend.group_requests.remove(group)
    group.member_requests.remove(friend)

    group_list = []
    group_list.append(group.name)

    return JsonResponse(group_list, safe=False)


def group_invitation_accepted(request):
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

    return JsonResponse(group_list, safe=False)


def leave_group(request):
    pk = request.GET.get('pk')
    group = Group.objects.get(pk=pk)
    print group
    group.members.remove(request.user.profile)

    group_list = []
    group_list.append(group.name)

    return JsonResponse(group_list, safe=False)


def can_come(request):
    pk = request.GET.get('pk', '')
    event = Event.objects.get(pk=pk)
    event.people_not_coming.remove(request.user.profile)
    event.people_coming.add(request.user.profile)
 
    hosts = ""
    host_list = [e for e in event.host.all()]
    for count, e in enumerate(host_list):
        if count >= len(host_list)-1:
            hosts += "%s" % e
        else:
            hosts += "%s, " % e
    date = "%s at %s" % (event.date_happening.strftime('%A, %b %-d'), event.time_starting.strftime('%-I:%M %p'))
    posted = "%s" % event.date_posted.isoformat(' ')
    return JsonResponse([event.name, hosts, date, "People coming: %d" % event.people_coming.count(), host_list[0].picture.url, posted, event.description, "People not coming: %d" % event.people_not_coming.count()], safe=False)


def cannot_come(request):
    pk = request.GET.get('pk', '')
    event = Event.objects.get(pk=pk)
    event.people_coming.remove(request.user.profile)
    event.people_not_coming.add(request.user.profile)
    hosts = ""
    host_list = [e for e in event.host.all()]
    for count, e in enumerate(host_list):
        if count >= len(host_list)-1:
            hosts += "%s" % e.first_name
        else:
            hosts += "%s, " % e.first_name
    date = "%s at %s" % (event.date_happening.strftime('%a, %b %-d'), event.time_starting.strftime('%-I:%M %p'))
    return JsonResponse([event.name, hosts, date, event.people_coming.count(), host_list[0].picture.url], safe=False)


def cancel_decision(request):
    pk = request.GET.get('pk', '')
    event = Event.objects.get(pk=pk)
    event.people_coming.remove(request.user.profile)
    event.people_not_coming.remove(request.user.profile)
    hosts = ""
    host_list = [e for e in event.host.all()]
    for count, e in enumerate(host_list):
        if count >= len(host_list)-1:
            hosts += "%s" % e
        else:
            hosts += "%s, " % e
    date = "%s at %s" % (event.date_happening.strftime('%A, %b %-d'), event.time_starting.strftime('%-I:%M %p'))
    posted = "%s" % event.date_posted.isoformat(' ')
    return JsonResponse([event.name, hosts, date, event.people_coming.count(), host_list[0].picture.url, posted, event.description], safe=False)


def clear_notification(request):
    pk = request.GET.get('pk', '')
    notif = Notification.objects.get(pk=pk)
    notif.read = True
    notif.save()
    return JsonResponse([request.user.profile.unread_notifications().count(),], safe=False)


def ajax_friends(request):
    context = {}
    pk = request.GET.get('group_pk')
    group = Group.objects.get(pk=pk)
    context['group'] = group
    member_ids = group.members.all().values_list('pk', flat=True)
    friends = request.user.profile.friends.exclude(pk__in=member_ids)
    context['friends'] = friends

    return render_to_response('friend_invite.html', context, context_instance=RequestContext(request))


def slugify(string):
    return string.lower().replace(' ', '-')


