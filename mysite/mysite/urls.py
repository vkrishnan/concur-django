from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'tweet.views.home', name='home'),
    url(r'^callback/', 'tweet.views.handle_callback', name='callback'),
    url(r'^get_request_token/$', 'tweet.views.get_request_token', name='callback'),
    url(r'^send/$', 'tweet.views.send', name='send'),
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
]
