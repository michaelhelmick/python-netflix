#!/usr/bin/env python

""" Python-Netflix """
'''
For Netflix API documentation, visit: http://developer.netflix.com/docs
'''

__author__ = 'Mike Helmick <mikehelmick@me.com>'
__version__ = '0.1.1'

import urllib
import httplib2
import oauth2 as oauth

try:
    from urlparse import parse_qsl
except ImportError:
    from cgi import parse_qsl

try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        try:
            from django.utils import simplejson as json
        except ImportError:
            raise ImportError('A json library is required to use this python library. Lol, yay for being verbose. ;)')


class NetflixAPIError(Exception): pass
class NetflixAuthError(NetflixAPIError): pass


class NetflixAPI(object):
    def __init__(self, api_key=None, api_secret=None, oauth_token=None, oauth_token_secret=None, callback_url=None, headers=None, client_args=None):
        if not api_key or not api_secret:
            raise NetflixAPIError('Please supply an api_key and api_secret.')

        self.api_key = api_key
        self.api_secret = api_secret
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.callback_url = callback_url

        self.request_token_url = 'http://api.netflix.com/oauth/request_token'
        self.access_token_url = 'http://api.netflix.com/oauth/access_token'
        self.authorize_url = 'https://api-user.netflix.com/oauth/login'

        self.api_base = 'http://api.netflix.com/'

        self.headers = headers
        if self.headers is None:
            self.headers = {'User-agent': 'Python-Netflix v%s' % __version__}

        self.consumer = None
        self.token = None

        client_args = client_args or {}

        if self.api_key is not None and self.api_secret is not None:
            self.consumer = oauth.Consumer(self.api_key, self.api_secret)

        if self.oauth_token is not None and self.oauth_token_secret is not None:
            self.token = oauth.Token(oauth_token, oauth_token_secret)

        # Filter down through the possibilities here - if they have a token, if they're first stage, etc.
        if self.consumer is not None and self.token is not None:
            self.client = oauth.Client(self.consumer, self.token, **client_args)
        elif self.consumer is not None:
            self.client = oauth.Client(self.consumer, **client_args)
        else:
            # If they don't do authentication, but still want to request unprotected resources, we need an opener.
            self.client = httplib2.Http(**client_args)

    def get_authentication_tokens(self):
        """ Returns an authentication tokens, which includes an 'auth_url' for the user to hit.
        """

        request_args = {}
        resp, content = self.client.request('%s?oauth_callback=%s' % (self.request_token_url, self.callback_url), 'GET', **request_args)

        if resp['status'] != '200':
            raise NetflixAuthError('There was a problem retrieving an authentication url.')

        request_tokens = dict(parse_qsl(content))

        auth_url_params = {
            'oauth_token': request_tokens['oauth_token'],
            'oauth_callback': self.callback_url,
            'oauth_consumer_key': self.api_key,
        }

        request_tokens['auth_url'] = '%s?%s' % (self.authorize_url, urllib.urlencode(auth_url_params))
        return request_tokens

    def get_auth_tokens(self, oauth_verifier=None):
        """ Returns 'final' tokens to store and used to make authorized calls to Netflix.
        """

        if not oauth_verifier:
            raise NetflixAuthError('No OAuth Verifier supplied.')

        params = {
            'oauth_verifier': oauth_verifier,
        }

        resp, content = self.client.request('%s?%s' % (self.access_token_url, urllib.urlencode(params)), 'GET')
        if resp['status'] != '200':
            raise NetflixAuthError('Getting access tokens failed: %s Response Status' % resp['status'])

        return dict(parse_qsl(content))

    def api_request(self, endpoint=None, method='GET', params=None, format='json', user=True):
        if endpoint is None:
            raise NetflixAPIError('Please supply an API endpoint.')

        if endpoint.startswith(self.api_base):
            url = endpoint
        else:
            url = self.api_base + endpoint

        if format == 'json':
            params.update({'output': 'json'})

        if method != 'GET':
            resp, content = self.client.request('%s?output=json' % url, method, body=urllib.urlencode(params), headers=self.headers)
        else:
            resp, content = self.client.request('%s?%s' % (url, urllib.urlencode(params)), 'GET', headers=self.headers)

        status = int(resp['status'])

        #try except for if content is able to be decoded
        try:
            content = json.loads(content)
        except json.JSONDecodeError:
            raise NetflixAPIError('Content is not valid JSON, unable to be decoded.')

        if status < 200 or status >= 300:
            raise NetflixAPIError('Code %d: %s' % (status, content['status']['message']))

        return dict(content)

    def get(self, endpoint=None, params=None):
        params = params or {}
        return self.api_request(endpoint, params=params)

    def post(self, endpoint=None, params=None):
        params = params or {}
        return self.api_request(endpoint, method='POST', params=params)

    def delete(self, endpoint=None, params=None):
        params = params or {}
        return self.api_request(endpoint, method='DELETE', params=params)
