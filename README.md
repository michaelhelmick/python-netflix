#Overview
I've been writing up APIs interfacing with OAuth in Python like no other the past week or so, so here is another... Netflix API.

Hope this documentation explains everything you need to get started. Any questions feel free to email me or inbox me.

#Authorization URL
*Get an authorization url for your user*

```python
n = NetflixAPI(api_key='*your app key*',
               api_secret='*your app secret*',
               callback_url='http://www.example.com/callback/')

auth_props = n.get_authentication_tokens()
auth_url = auth_props['auth_url']

#Store this token in a session or something for later use in the next step.
oauth_token_secret = auth_props['oauth_token_secret']

print 'Connect with Netflix via %s' % auth_url
```

Once you click "Allow" be sure that there is a URL set up to handle getting finalized tokens and possibly adding them to your database to use their information at a later date. \n\n'

#Handling the callback
```python
# In Django, you'd do something like
# oauth_token = request.GET.get('oauth_verifier')
# oauth_verifier = request.GET.get('oauth_verifier')

oauth_token = *Grab oauth token from URL*
oauth_verifier = *Grab oauth verifier from URL*

#Initiate the NetflixAPI class in your callback.
n = NetflixAPI(api_key='*your app key*',
               api_secret='*your app secret*',
               oauth_token=oauth_token,
               oauth_token_secret=session['netflix_session_keys']['oauth_token_secret'])

authorized_tokens = n.get_auth_tokens(oauth_verifier)

final_oauth_token = authorized_tokens['oauth_token']
final_oauth_token_secret = authorized_tokens['oauth_token_secret']
final_user_id = authorized_tokens['user_id']

# Save those tokens and user_id to the database for a later use?
```

#Getting some user information
```python
# Get the final tokens from the database or wherever you have them stored

n = NetflixAPI(api_key = '*your app key*',
               api_secret = '*your app secret*',
               oauth_token=final_tokens['oauth_token'],
               oauth_token_secret=final_tokens['oauth_token_secret'],
               user_id=final_tokens['user_id'])

# Return a list of the users Instant Queue.
instant_queue = n.get('queues/instant')
print instant_queue

# Add Gabriel Iglesias: Hot and Fluffy to Instant Queue
add_to_queue = n.post('queues/instant', params={'title_ref': 'http://api.netflix.com/catalog/titles/movies/70072945'}) #You can also added "position" to the params to set where this media will be positioned on the users queue.

#This returns the added item if successful.
# If it's already in the queue, it will return a NetflixAPIError, code 412
print add_to_queue

# Remove Gabriel Iglesias: Hot and Fluffy to Instant Queue
## When querying for the users Queue, when iterating over the Queue items
## you can use the 'id' for the next call. Where it says *CURRENT_USER_ID*
## that is automatically returned from the Netflix Instant Queue response.
del_from_queue = n.delete('http://api.netflix.com/users/*CURRENT_USER_ID*/queues/instant/available/2/70072945')

print del_from_queue
```