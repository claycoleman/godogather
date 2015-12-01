import datetime

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm, UserChangeForm

from .models import Event, Group, Profile

#Event forms

class EventModelCreateForm(forms.ModelForm):
    date_happening = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), initial=datetime.datetime.now())
    time_starting = forms.TimeField(widget=forms.TimeInput(attrs={'type':'time'}), initial=datetime.datetime.now())
    time_ending = forms.TimeField(widget=forms.TimeInput(attrs={'type':'time'}), initial=datetime.datetime.now())

    class Meta:
        model = Event
        exclude = ['date_posted', 'people_coming', 'people_not_coming']

    def __init__(self, *args, **kwargs):
        super(EventModelCreateForm, self).__init__(*args, **kwargs)
        self.fields["host"].widget = forms.CheckboxSelectMultiple()
        self.fields["groups"].widget = forms.CheckboxSelectMultiple()


class EventModelUpdateForm(forms.ModelForm):  

    date_happening = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), initial=datetime.datetime.now())
    time_starting = forms.TimeField(widget=forms.TimeInput(attrs={'type':'time'}), initial=datetime.datetime.now())
    time_ending = forms.TimeField(widget=forms.TimeInput(attrs={'type':'time'}), initial=datetime.datetime.now())

    class Meta:
        model = Event
        exclude = ['date_posted', 'people_coming', 'people_not_coming']

    def __init__(self, *args, **kwargs):
        super(EventModelUpdateForm, self).__init__(*args, **kwargs)
        self.fields["host"].widget = forms.CheckboxSelectMultiple()
        self.fields["groups"].widget = forms.CheckboxSelectMultiple()



#Group forms
class GroupModelCreateForm(forms.ModelForm):  
    class Meta:
        model = Group
        exclude = ['members']

    def __init__(self, *args, **kwargs):
        super(GroupModelCreateForm, self).__init__(*args, **kwargs)
        self.fields["member_requests"].widget = forms.CheckboxSelectMultiple()
        self.fields["admin"].widget = forms.CheckboxSelectMultiple()


class GroupModelUpdateForm(forms.ModelForm):  
    class Meta:
        model = Group
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(GroupModelUpdateForm, self).__init__(*args, **kwargs)
        self.fields["member_requests"].widget = forms.CheckboxSelectMultiple()
        self.fields["members"].widget = forms.CheckboxSelectMultiple()

        self.fields["admin"].widget = forms.CheckboxSelectMultiple()



#Profile / User forms
class SearchProfile(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'id': 'search', 'placeholder': 'Search for friends!', 'class': 'form-control'}))


class UserLogin(forms.Form):  
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class UserModelCreateForm(UserCreationForm):  
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        new_user = super(UserCreateForm, self).save(commit=False)
        new_user.email = self.cleaned_data["email"]
        new_profile = Profile.objects.create(user=new_user)
        new_profile.save()
        if commit:
            new_user.save()
        return user


class UserModelUpdateForm(UserChangeForm):  
    class Meta:
        model = User
        exclude = ['name']


class ProfileModelCreateForm(forms.ModelForm):  
    class Meta:
        model = Profile
        exclude = ['user']


class ProfileModelUpdateForm(forms.ModelForm):  
    class Meta:
        model = Profile
        exclude = ['user', 'past_events', 'friends', 'friend_requests']


class ContactForm(forms.Form):
    author = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'author', 'placeholder': 'Your name *', 'class': 'form-control'}))
    comment = forms.CharField(required=True, widget=forms.Textarea(attrs={'id': 'comment', 'placeholder': 'Your message *', 'class': 'form-control', 'rows': '4'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'id': 'email', 'placeholder': 'Your email *', 'class': 'form-control'}))



class JQueryUIDatepickerWidget(forms.DateInput):
    def __init__(self, **kwargs):
        super(forms.DateInput, self).__init__(attrs={"size":10, "class": "dateinput"}, **kwargs)

    class Media:
        css = {"all":("http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/themes/redmond/jquery-ui.css",)}
        js = ("http://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js",
              "http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/jquery-ui.min.js",)
