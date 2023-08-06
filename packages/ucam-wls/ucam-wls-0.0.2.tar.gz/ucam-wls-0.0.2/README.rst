============================================
ucam-wls: a Raven-like login service library
============================================

`Documentation <#>`_ [todo] |
`PyPI <#>`_ [todo] |
`GitHub <https://github.com/edwinbalani/ucam-wls>`_

``ucam-wls`` is a Python library to implement the *web login service* (WLS)
component of the 'Ucam-WebAuth' (or 'WAA2WLS') protocol, which is used
primarily at the University of Cambridge as part of the `Raven authentication
service`_.

-------------------------------------------------------------------------------


Introduction
------------

There are many implementations of the 'web authentication agent' (WAA) part of
Ucam-WebAuth.  These are run by the party that is requesting a user's identity,
and they exist already for various platforms, applications and languages.

Examples include:

- the officially-supported `mod_ucam_webauth`_ module for Apache Web Server,
  which is very popular (at least within Cambridge University)
- `ucam-webauth-php`_, also published by the University but "not (officially)
  supported"
- Daniel Richman's `python-ucam-webauth`_
- `django-ucamwebauth`_, which is written and maintained by a team within the
  University

(More are listed on the `Raven project page`_.)

However, no known implementations of the WLS component (which authenticates
users against known credentials) exist, apart from the official Raven
`production`_ and `test/demo`_ servers.

``ucam-wls`` is a first attempt at a solution for developing your own WLS.  It
is intended to be easily integrated into a custom or in-house application to
provide the full authentication service.

.. _Ucam-WebAuth: https://raven.cam.ac.uk/project/waa2wls-protocol.txt
.. _Raven authentication service: https://raven.cam.ac.uk/project/
.. _Raven project page: https://raven.cam.ac.uk/project/
.. _mod_ucam_webauth: https://github.com/cambridgeuniversity/mod_ucam_webauth
.. _ucam-webauth-php: https://github.com/cambridgeuniversity/ucam-webauth-php
.. _python-ucam-webauth: https://github.com/DanielRichman/python-ucam-webauth
.. _django-ucamwebauth: https://github.com/uisautomation/django-ucamwebauth
.. _production: https://raven.cam.ac.uk/
.. _test/demo: https://demo.raven.cam.ac.uk/


Potential applications
----------------------

An **internal single sign-on** service:

- Useful for systems with in-house user account bases: internal webapps avoid
  reinventing the wheel by using battle-tested WAA implementations.
- Easier to develop an internal login system in this way: half the work (the
  WAA side) is already done.
- Internal webapps no longer need to roll their own authentication
  systems/databases, and access to passwords can be kept in a centralised
  location.
- *Sounds a lot like the Raven service*, but webapps can authenticate against
  an entirely different user database.

**Two-headed** login service:

- Users can authenticate using either locally-administered credentials, or by
  being 'referred' to Raven (where the WLS redirects the client browser to
  Raven using the same request parameters).
- Integrates authentication of local guest, external or special (e.g.
  administrator) accounts with that of mainstream Raven users, creating
  a unified login process regardless of the 'source' of the user's identity.
- Similar to local *vs.* Raven login options on many websites and CMSes, but
  can be managed institution-wide rather than having to maintain decoupled sets
  of passwords on each installation of WordPress, Drupal, *etc.*

The above two use-cases essentially offer the same benefits that Raven does,
but with the added advantage that users don't need a Raven account to benefit
(*e.g.* guests, external researchers, former staff/alumni).  Alternatively, if
they do have a Raven account, they can be given the option of using Raven or
local credentials.

The next use-case is different...

**Stricter authentication requirements** than what Raven provides:

- Useful for sensitive applications
- Require both a username/password (possibly from either Raven or local
  credentials; see above) as well as multi-factor authentication methods such
  as a one-time password (OTP).
- OTP secrets can be kept and managed centrally; the webapp never sees them or
  the OTP responses.


Example WLS implementation
--------------------------

A simple implementation of a WLS using this library, and similar in nature to
the `Raven demo server`_, is available in the `wls-demo`_ repository.

.. _Raven demo server: https://demo.raven.cam.ac.uk/
.. _wls-demo: https://github.com/edwinbalani/wls-demo


Contributing
------------

There is a long **to-do list** on this project.  It includes:

* Writing unit tests
* Refining documentation of the public API, and getting a Read the Docs site
  going.
* Providing an example implementation of a WLS using the library (possibly in
  another repository, or bundled into the ``ucam-wls`` Python package).
  **Importantly**, the Raven demo key (with key ID 901), with its publicly
  disclosed private key, should be used to signify that no useful
  authentication information is provided.

If you are keen to help out on any of the above (or indeed anything else), then
please fork, commit and submit a pull request!  Maybe `get in touch
<git+ucam-wls@balani.xyz>`_ too :)


A warning
---------

``ucam-wls`` is currently **experimental, pre-alpha quality software**.  It has
not been tested heavily (yet), and no guarantees can be made regarding its
security or robustness.

For example, while the library attempts to make *some* checks on input
arguments (regarding types, values, validity *etc.*), it is still definitely
possible to produce bogus responses that will confuse WAAs.  (However,
``ucam-wls`` is a library, and there is some level of expectation that
application developers will interface with it properly!)


What this library does and doesn't do
-------------------------------------

``ucam-wls`` is a *library*, not a complete solution.  Accordingly, it will:

* Provide a **high-level interface** to a protocol-compliant implementation of
  a WLS.
* Accept authentication requests as URL **query strings**, a Python
  **dictionary** of parameters, or as **keyword arguments** to a class
  constructor function.
* Generate signed authentication responses with the appropriate status code,
  using a provided RSA private key.

But ``ucam-wls`` *won't*:

* Run a fully-blown authentication server that checks usernames/passwords.
* Serve a web interface for users to authenticate.  (See `wls-demo`_ for an
  example of this.)
* Manage your RSA private keys for you.


Links
-----

- `WAA2WLS protocol definition <https://github.com/cambridgeuniversity/UcamWebauth-protocol/blob/master/waa2wls-protocol.txt>`_
- `Raven project pages <https://raven.cam.ac.uk/project/>`_
- `Raven wiki <https://wiki.cam.ac.uk/raven/>`_.  Contains lots of newer
  information on Raven support, WAA implementations, *etc.*


Credits and copyright
---------------------

``ucam-wls`` is authored by `Edwin Balani <https://github.com/edwinbalani/>`_,
and released under the terms of the MIT License.

The Ucam-WebAuth/WAA2WLS protocol was designed by `Jon Warbrick
<http://people.ds.cam.ac.uk/jw35/>`_.
