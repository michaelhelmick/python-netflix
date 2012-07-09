Python-Netflix
==============

Python-Netflix is a Python Library to interface with `Netflix REST API <http://developer.netflix.com/docs/REST_API_Reference>`_ & OAuth

Features
--------

* Retrieve user information
* Retrieve queue information
* Add items to queue
* And many more, supports all REST endpoints


Installation
------------

Installing Python-Netflix is simple: ::

    $ pip install python-netflix

Usage
-----

Authorization URL
~~~~~~~~~~~~~~~~~
::

    n = NetflixAPI(api_key='*your app key*',
                    api_secret='*your app secret*',
                    callback_url='http://www.example.com/callback/')

    auth_props = n.get_authentication_tokens()
    auth_url = auth_props['auth_url']

    #Store this token in a session or something for later use in the next step.
    oauth_token_secret = auth_props['oauth_token_secret']

    print 'Connect with Netflix via %s' % auth_url

Once you click "Allow" be sure that there is a URL set up to handle getting finalized tokens and possibly adding them to your database to use their information at a later date.

Handling the callback
~~~~~~~~~~~~~~~~~~~~~
::

    # In Django, you'd do something like
    # oauth_token = request.GET.get('oauth_verifier')
    # oauth_verifier = request.GET.get('oauth_verifier')
    
    oauth_token = *Grab oauth token from URL*
    oauth_verifier = *Grab oauth verifier from URL*
    
    #Initiate the NetflixAPI class in your callback.
    n = NetflixAPI(api_key='*your app key*',
                   api_secret='*your app secret*',
                   oauth_token=oauth_token,
                   oauth_token_secret=session['netflix_session_keys'][  'oauth_token_secret'])
    
    authorized_tokens = n.get_auth_tokens(oauth_verifier)
    
    final_oauth_token = authorized_tokens['oauth_token']
    final_oauth_token_secret = authorized_tokens['oauth_token_secret']
    final_user_id = authorized_tokens['user_id']

Save those tokens and user_id to the database for a later use?

Return a list of the users Instant Queue
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    n = NetflixAPI(api_key = '*your app key*',
                    api_secret = '*your app secret*',
                    oauth_token=final_tokens['oauth_token'],
                    oauth_token_secret=final_tokens['oauth_token_secret'])

    instant_queue = n.get('users/*final_user_id*/queues/instant')
    print instant_queue

Add Gabriel Iglesias: Hot and Fluffy to Instant Queue
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    # Assume you are using the same NetflixAPI instance as above
    try:
        add_to_queue = n.post('users/*final_user_id*/queues/instant', params={'title_ref': 'http://api.netflix.com/catalog/titles/movies/70072945'})

        print add_to_queue

        # You can also added "position" to the params to set where this media will be positioned on the users queue.
    except NetflixAPIError:
        # This returns the added item if successful.
        # If it's already in the queue, it will return a NetflixAPIError, code 412 

Remove Gabriel Iglesias: Hot and Fluffy to Instant Queue
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    # Assume you are using the same NetflixAPI instance as above
    # When querying for the users Queue, when iterating over the Queue items
    # you can use the 'id' for the next call. Where it says *final_user_id*
    # that is automatically returned from the Netflix Instant Queue response.

    del_from_queue = n.delete('http://api-public.netflix.com/users/*final_user_id*/queues/instant/available/2/70072945')

    print del_from_queue

Rate Gabriel Iglesias: Hot and Fluffy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

    try:
        # Create a new rating
        create_rating = n.post('users/*final_user_id*/ratings/title/actual/70072945', params={'rating': '5'})

        print create_rating
    except NetflixAPIError:
        # This returns a status message if successful.
        # If it's already been rated, it will return a NetflixAPIError, code 422
        pass


    # Update/Clear rating
    update_rating = n.put('users/*final_user_id*/ratings/title/actual/70072945', params={'rating': 'no_opinion'})

    print update_rating