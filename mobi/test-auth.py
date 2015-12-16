#! /usr/bin/env python

import requests, os, sys

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

from main.models import Profile

import django
django.setup()

# username = 'root'
# password = 'nimda'

# prof = Profile.objects.get(username=username)

# response = requests.post('http://127.0.0.1:8000/api-token-auth/', data={'username': username, 'password': password})

# data = response.json()
# token = data['token']

# print token

# headers = {'Authorization': 'Token %s' % token}

# response = requests.get('http://127.0.0.1:8000/api/profile/%s/' % prof.pk, headers=headers)

# print response
# print response.text

# response = requests.post('http://127.0.0.1:8000/auth/token', data={'client_id': 'glRG52YYhSeRARgXzuqjbTtqsIcC5ISDaB1J5VMZ', 'client_secret': 'AhnbNqcJTbW7D0nbHNNrW6vn6BSyDHiwj36k9OnJFV0yaiM8HDtrBn1dkMLbiCKukuFOg6UQ6yBoNSglzKoKDv89JX8OkhMYNlTn6gCfWL4brhVWfCjqphGpjAvBv6Zv', 'grant_type': 'password', 'username':username, 'password': password})

# print response

# data = response.json()
# access_token = data['access_token']
# print "Access token", access_token

# response = requests.post('http://127.0.0.1:8000/auth/convert-token', 
#     data={'client_id': 'glRG52YYhSeRARgXzuqjbTtqsIcC5ISDaB1J5VMZ', 
#             'client_secret': 'AhnbNqcJTbW7D0nbHNNrW6vn6BSyDHiwj36k9OnJFV0yaiM8HDtrBn1dkMLbiCKukuFOg6UQ6yBoNSglzKoKDv89JX8OkhMYNlTn6gCfWL4brhVWfCjqphGpjAvBv6Zv', 
#             'grant_type': 'convert_token', 
#             'backend': 'oauth2',
#             'token': access_token 
#             })


# print response
# print response.text
# # token = data['access_token']

# headers = {'Authorization': 'Token %s' % access_token}

# response = requests.get('http://127.0.0.1:8000/api/profile/%s/' % prof.pk, headers=headers)

# print response
# print response.text

    # data={'client_id': 'glRG52YYhSeRARgXzuqjbTtqsIcC5ISDaB1J5VMZ', 
    #         'client_secret': 'AhnbNqcJTbW7D0nbHNNrW6vn6BSyDHiwj36k9OnJFV0yaiM8HDtrBn1dkMLbiCKukuFOg6UQ6yBoNSglzKoKDv89JX8OkhMYNlTn6gCfWL4brhVWfCjqphGpjAvBv6Zv', 
    #         'grant_type': 'convert_token', 
    #         'backend': 'facebook',
    #         'token': prof.user.social_auth.get(provider='facebook').extra_data.get('access_token')
    #         })


prof = Profile.objects.get(first_name='Clay')

headers = {'Authorization': 'Bearer facebook %s' % prof.user.social_auth.get(provider='facebook').extra_data['access_token']}

# response = requests.get('http://127.0.0.1:8000/api/feed/', headers=headers)
# response = requests.get('http://127.0.0.1:8000/api/profile/%s/' % prof.pk, headers=headers)

response = requests.post('http://127.0.0.1:8000/auth/convert-token', 

    data={'client_id': 'glRG52YYhSeRARgXzuqjbTtqsIcC5ISDaB1J5VMZ', 
            'client_secret': 'AhnbNqcJTbW7D0nbHNNrW6vn6BSyDHiwj36k9OnJFV0yaiM8HDtrBn1dkMLbiCKukuFOg6UQ6yBoNSglzKoKDv89JX8OkhMYNlTn6gCfWL4brhVWfCjqphGpjAvBv6Zv', 
            'grant_type': 'convert_token', 
            'backend': 'facebook',
            'token': prof.user.social_auth.get(provider='facebook').extra_data.get('access_token')
            })


print response

data = response.json()
token = data['access_token']

print token

headers = {'Authorization': 'Token %s' % token}
response = requests.get('http://127.0.0.1:8000/api/feed/', headers=headers)

print response
print response.text
