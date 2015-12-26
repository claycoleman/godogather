import os
from location_picker import LocationField
from datetime import datetime
from icalendar import Calendar
from icalendar import Event as CalEvent

from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


class Event(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(null=True, blank=True, max_length=255)
    test_location = LocationField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_happening = models.DateField(null=True, blank=True)
    time_starting = models.TimeField(null=True, blank=True)
    time_ending = models.TimeField(null=True, blank=True)
    people_coming = models.ManyToManyField('Profile', blank=True, related_name="events_going_to")
    people_not_coming = models.ManyToManyField('Profile', blank=True, related_name="events_not_going_to")
    host = models.ManyToManyField('Profile', blank=True, related_name="events_hosted")
    groups = models.ManyToManyField('Group', blank=True)
    public = models.BooleanField(default=True)
    shareable = models.BooleanField(default=True)
    ics = models.FileField(upload_to="event_ics", null=True, blank=True)
    invitees = models.ManyToManyField('Profile', blank=True, related_name='events_invited_to')

    def __unicode__(self):
        if not self.name:
            return "this event"
        return self.name


    def create_apple_ics(self):
        url_date_starting = datetime.combine(date=self.date_happening, time=self.time_starting).isoformat().replace('-', '').replace(':', '')
        url_date_ending = datetime.combine(date=self.date_happening, time=self.time_ending).isoformat().replace('-', '').replace(':', '')

        try:
            os.remove(self.ics.file.name)
        except:
            pass

        cal = Calendar()

        app_event = CalEvent()
        app_event['summary'] = self.name
        app_event['location'] = self.location
        app_event['uid'] = self.pk
        app_event['dtstart'] = url_date_starting
        app_event['dtend'] = url_date_ending
        cal.add_component(app_event)

        self.ics.save('{0}.ics'.format(self.pk), ContentFile(cal.to_ical()))

    class Meta:
        ordering = ['date_happening']


class Profile(models.Model):
    user = models.OneToOneField(User)
    new_user = models.BooleanField(default=True)
    first_name = models.CharField(null=True, blank=True, max_length=255)
    last_name = models.CharField(null=True, blank=True, max_length=255)
    username = models.CharField(null=True, blank=True, max_length=255)
    bio = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to="profile_pictures", null=True, blank=True)
    friends = models.ManyToManyField('Profile', blank=True, related_name="+")
    events_posted = models.ManyToManyField('Event', blank=True, related_name="people_who_posted_it")
    shared_events = models.ManyToManyField('Event', blank=True, related_name="people_who_shared_it")
    group_requests = models.ManyToManyField('Group', blank=True, related_name="invited_people")
    friend_requests = models.ManyToManyField('Profile', blank=True, related_name="requested_friends")
    past_events = models.ManyToManyField('Event', blank=True, related_name="+")
    followers = models.ManyToManyField('Profile', blank=True, related_name="people_you_follow")
    
    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        if self.first_name:
            self.first_name = self.first_name.strip(" ")
            self.last_name = self.last_name.strip(" ")
            self.username = self.username.strip(" ")
            if " " in self.first_name:
                self.first_name, space, temp = self.first_name.partition(" ")
                self.last_name = temp + " " + self.last_name
            super(Profile, self).save(*args, **kwargs) # Call the "real" save() method.

    def unread_notifications(self):
        if self.notifications.exists():
            return self.notifications.filter(read=False)
        return []


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Group(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    member_requests = models.ManyToManyField('Profile', blank=True, related_name="requested_groups")
    members = models.ManyToManyField('Profile', blank=True, related_name='groups_in')
    admin = models.ManyToManyField('Profile', blank=True, related_name="groups_admined")
    searchable = models.BooleanField(default=False)
    open_group = models.BooleanField(default=True)
    admin_only = models.BooleanField(default=False)
    followers = models.ManyToManyField('Profile', blank=True, related_name="groups_you_follow")

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __unicode__(self):
        return self.name

    def admin_already_members(self):
        if self.admin.exists():
            return self.admin.filter(pk__in=self.members.all().values_list('pk', flat=True))
        return []


class Comment(models.Model):
    message = models.CharField(null=True, blank=True, max_length=255)
    event = models.ForeignKey('Event', null=True, blank=True)
    author = models.ForeignKey('Profile', null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    comment_in_response_to = models.ForeignKey('Comment', null=True, blank=True, related_name="replies")

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __unicode__(self):
        if self.author and self.event:
            return "%s about %s" % (self.author, self.event)
        return "Generic comment"
    

class Notification(models.Model):
    notification_type = models.CharField(null=True, blank=True, max_length=255)
    message = models.CharField(null=True, blank=True, max_length=255)
    sender_pk = models.CharField(null=True, blank=True, max_length=255)
    user = models.ForeignKey('Profile', null=True, blank=True, related_name='notifications')
    read = models.BooleanField(default=False)
    date_notified = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-date_notified']

    def __unicode__(self):
        if not self.message:
            return 'Uh oh'
        return self.message


class FriendList(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)
    owner = models.ForeignKey('Profile', null=True, blank=True, related_name='lists')
    people = models.ManyToManyField('Profile', blank=True, related_name='+')
    contacts = models.ManyToManyField('Contact', blank=True, related_name='+')

    class Meta:
        verbose_name = "List"
        verbose_name_plural = "Lists"
        ordering = ['name']

    def __unicode__(self):
        if not self.name:
            return 'Uh oh'
        return self.name


class Contact(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)
    contact_method = models.CharField(null=True, blank=True, max_length=255)
    creator = models.ForeignKey('Profile', null=True, blank=True, related_name='user_contacts')

    def __unicode__(self):
        return self.name or "Uh oh"
