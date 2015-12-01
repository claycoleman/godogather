from django.contrib import admin
from .models import Event, Profile, Group


class EventAdmin(admin.ModelAdmin):
    '''
        Admin View for Event
    '''
    list_display = ('name', 'date_happening',)
    list_filter = ('name', 'date_posted',)
    search_fields = ['']


class GroupAdmin(admin.ModelAdmin):
    '''
        Admin View for Group
    '''
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ['name']


class ProfileAdmin(admin.ModelAdmin):
    '''
        Admin View for Profile
    '''
    list_display = ('user',)
    list_filter = ('user',)
    search_fields = ['user']

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Event, EventAdmin)
