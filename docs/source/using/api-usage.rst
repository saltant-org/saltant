API usage
==========

An API reference for saltant is available at at
`saltant-org.github.io/saltant`_. Use it. It's super useful.

There's also a Python SDK for saltant, `saltant-py`_, which makes
interacting with the API a lot easier (given that you're using Python).
Check it out.

Authentication
--------------

By default you need to be authenticated to access anything on the
API. There are three ways to authenticate:

#. JWT authentication
#. Token authentication
#. Session authentication

**JWT authentication**

To obtain an access and refresh JTW pair, you need to provide your
username and password to `/token/`_. To obtain a new access token with
your refresh token, provide your refresh token to `/token/refresh/`_.
Refresh and access tokens have a default lifetime of 35 weeks and 3
days, respectively (although this will likely vary with saltant
implementations).

Then, to make any HTTP request to saltant, include your JTW access token
in the Authorization header like so::

    Authorization: Bearer myaccesstokenhere

**Token authentication**

Authorization tokens can only be obtained from an administrator. But
once you have one, your Authorization header should look like ::

    Authorization: Token myauthtokenhere

**Session authentication**

Session authentication is used with the browsable API. To authenticate
yourself, you simply need to log in.

.. Links
.. _saltant-py: https://github.com/saltant-org/saltant-py/
.. _saltant-org.github.io/saltant: https://saltant-org.github.io/saltant/

.. API links
.. _/token/: https://saltant-org.github.io/saltant/#operation/token_create
.. _/token/refresh/: https://saltant-org.github.io/saltant/#operation/token_refresh_create
