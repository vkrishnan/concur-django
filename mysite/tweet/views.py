from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.shortcuts import redirect
from mysite import settings
from json import loads

import pyowm
import urlparse
import requests
import oauth2
import urllib3

REQUEST_TOKEN={}
ACCESS_TOKEN={}

CONSUMER_KEY = settings.SOCIAL_AUTH_TWITTER_KEY
CONSUMER_SECRET = settings.SOCIAL_AUTH_TWITTER_SECRET

CONSUMER = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
MANAGER = urllib3.PoolManager()

def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content

def get_request_token(request):
    global REQUEST_TOKEN
    resp, content = oauth2.Client(CONSUMER).request('https://api.twitter.com/oauth/request_token', "GET")

    if resp['status'] != '200':
        print content
        raise Exception("Invalid response %s." % resp['status'])

    REQUEST_TOKEN = dict(urlparse.parse_qsl(content))

    return redirect("%s?oauth_token=%s" % ('https://api.twitter.com/oauth/authorize', REQUEST_TOKEN['oauth_token']))



def home(request):

    context = RequestContext(request,
                           	{'request': request,
                            'user': request.user})
    return render_to_response('home.html', 
                             context_instance=context)

def handle_callback(request):
    global ACCESS_TOKEN
    token = oauth2.Token(REQUEST_TOKEN['oauth_token'], REQUEST_TOKEN['oauth_token_secret'])
    print token
    token.set_verifier(request.GET.get('oauth_verifier'))
    client = oauth2.Client(CONSUMER, token)

    resp, content = client.request('https://api.twitter.com/oauth/access_token', "POST")
    ACCESS_TOKEN = dict(urlparse.parse_qsl(content))

    """ User now logged in so just redirect """
    return redirect("/")


def send(request):
    owm = pyowm.OWM('da83294f7abe6b4a55a1e2266829356c')
    observation = owm.weather_at_place('Bangalore, India')
    temperature = observation.get_weather().get_temperature(unit='celsius')['temp']

    posting_message = 'Bangalore%20temperature%20is%20' + str(temperature)
    
    url_message= 'https://api.twitter.com/1.1/statuses/update.json?status=%s' %(posting_message)
    return_value = oauth_req(url_message, 
                            ACCESS_TOKEN['oauth_token'], ACCESS_TOKEN['oauth_token_secret'], 'POST')
    json_data = loads(return_value)
    print json_data

    return redirect("/")
