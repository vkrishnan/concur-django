from django.shortcuts import render_to_response
from django.template.context import RequestContext
from requests_oauthlib import OAuth1
from urlparse import parse_qs
from mysite import settings

import requests

def home(request):
    context = RequestContext(request,
                           	{'request': request,
                            'user': request.user})
    oauth = OAuth1(settings.SOCIAL_AUTH_TWITTER_KEY, client_secret=settings.SOCIAL_AUTH_TWITTER_SECRET)
    r = requests.post(url=settings.REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)

    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]

    # Authorize
    authorize_url = settings.AUTHORIZE_URL + resource_owner_key

    #auth = {}
    #auth['url'] = authorize_url
    #print auth
    return render_to_response('home.html', {'auth':{'url':authorize_url}},
                             context_instance=context)
