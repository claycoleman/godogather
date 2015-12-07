from requests import request, HTTPError

from django.core.files.base import ContentFile

from main.models import Profile

def save_profile_picture(backend, details, response, user, *args, **kwargs):
    if 'FacebookOAuth2' in str(backend.__class__):
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])

        try:
            response = request('GET', url, params={'type': 'large'})
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            profile, created = Profile.objects.get_or_create(user=user)
            if created:
                profile.picture.save('{0}_prof_pic.jpg'.format(user.username), ContentFile(response.content))
                profile.first_name = user.first_name
                profile.last_name = user.last_name
                profile.username = user.username
                profile.save()