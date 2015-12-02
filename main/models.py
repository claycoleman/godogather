from django.db import models
from django.contrib.auth.models import User
from location_picker import LocationField

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
    public = models.BooleanField(default=False)
    shareable = models.BooleanField(default=True)

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
    shared_events = models.ManyToManyField('Event', blank=True, related_name="people_who_shared")
    group_requests = models.ManyToManyField('Group', blank=True, related_name="requested_members")
    friend_requests = models.ManyToManyField('Profile', blank=True, related_name="requested_friends")
    past_events = models.ManyToManyField('Event', blank=True, related_name="+")

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.strip(" ")
        self.last_name = self.last_name.strip(" ")
        self.username = self.username.strip(" ")
        if " " in self.first_name:
            self.first_name, space, temp = self.first_name.partition(" ")
            self.last_name = temp + " " + self.last_name
        super(Profile, self).save(*args, **kwargs) # Call the "real" save() method.


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
