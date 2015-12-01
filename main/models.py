from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(null=True, blank=True, max_length=255)
    date_posted = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_happening = models.DateField(null=True, blank=True)
    time_starting = models.TimeField(null=True, blank=True)
    time_ending = models.TimeField(null=True, blank=True)
    people_coming = models.ManyToManyField('Profile', blank=True, related_name="events_going_to")
    people_not_coming = models.ManyToManyField('Profile', blank=True, related_name="events_not_going_to")
    host = models.ManyToManyField('Profile', blank=True, related_name="events_hosted")
    groups = models.ManyToManyField('Group', blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['date_happening']



class Profile(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(null=True, blank=True, max_length=255)
    last_name = models.CharField(null=True, blank=True, max_length=255)
    username = models.CharField(null=True, blank=True, max_length=255)
    bio = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to="profile_pictures", null=True, blank=True)
    friends = models.ManyToManyField('Profile', blank=True, related_name="+")
    group_requests = models.ManyToManyField('Group', blank=True, related_name="requested_members")
    friend_requests = models.ManyToManyField('Profile', blank=True, related_name="requested_friends")
    past_events = models.ManyToManyField('Event', blank=True, related_name="+")

    def __unicode__(self):
            return "%s %s" % (self.first_name, self.last_name)




class Group(models.Model):
    name = models.CharField(null=True, blank=True, max_length=255)
    member_requests = models.ManyToManyField('Profile', blank=True, related_name="requested_groups")
    members = models.ManyToManyField('Profile', blank=True, related_name='groups_in')
    admin = models.ManyToManyField('Profile', blank=True, related_name="groups_admined")

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __unicode__(self):
            return self.name
