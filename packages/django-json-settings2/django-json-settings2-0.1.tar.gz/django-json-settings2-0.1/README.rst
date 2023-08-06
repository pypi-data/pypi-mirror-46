.. |nlshield| image:: https://img.shields.io/badge/100%25-Netlandish-blue.svg?style=square-flat
              :target: https://www.netlandish.com

================================
django-json-settings2 |nlshield|
================================
:Info: Simple application to store Django settings in a json file.
:Version: 0.1.0
:Author: Team Netlandish (https://www.netlandish.com)

Python / Django Support
=======================

* Python 3.6+ for Django versions 1.11+

Truthfully, this app is so simple it will probably work with previous 
version of Python and Django but we can't promise that.

Why?
====

I know, right? Who needs another way to store settings outside of the 
standard Django ``settings.py`` setup.

None of the existing ways actually fit our typical Django deployment 
setup in a way that was satisfactory. This method allows us to store 
settings externally and in a way that fits our needs. Maybe it'll 
fit yours too.

Also, there is already a ``django-json-settings`` app and while that app 
very well may be perfect for your project, it isn't a good fit for ours.

We created this app years ago and simply tuned it slowly as needed. It's 
very simple yet flexible enough to work within virtually any workflow.

This app is really nothing more than helper functins wrapped on top 
of standard ``json`` module ops.

Others
======

There are several other options to store settings outside of the typical
Django ``settings.py`` file. Here are a few:

* https://github.com/isotoma/django-json-settings
* https://github.com/theskumar/python-dotenv

There's dozens of others. Pick the one that best suits your needs.

Usage
=====

Saving Settings
---------------

You're going to need to save your desired settings to a json file 
first. There's a simple helper function, and management command, 
included to help.

For instance, say you want to create a simple setting for your ``SECRET_KEY`` 
variable::

    $ python
    >>> settings_to_save = ['SECRET_KEY']
    >>> from json_settings2 import write_settings_from_django
    >>> write_settings_from_django(*settings_to_save)
    >>> exit()
    $ cat .settings.json
    {
        "SECRET_KEY": "SUPER SECRET KEY IS HERE! COOOOOOOLLLLL!"
    }
    $

The ``write_settings_from_django`` function takes a few optional variables:

* settings_vars = Positional args giving every Django setting to save
* filename = Filename of the json settings file. Defaults to ``.settings.json``
* directory = Directory in which to save ``filename``. Defaults to ``.``.
* indent = Indentation level for the json output. Set to ``None`` for the most 
           compact file. Defaults to ``4``.
* force = If ``directory``/``filename`` exists, overwrite it. 
          Defaults to ``False``

You can also just use the management command. This requires that you place
``json_settings2`` in your ``INSTALLED_APPS`` setting::

    $ python manage.py write_json_settings SECRET_KEY

You can add as many settings as you'd like too::

    $ python manage.py write_json_settings SECRET_KEY DATABASES STATIC_URL

To see the options, simply::

    $ python manage.py help write_json_settings

Loading Settings
----------------

The easiest way is to store all your default and local settings in 
``settings.py`` and load the json settings at the end. It's pretty 
straight forward. Let's see an example::

    $ cat settings.py
    import os
    from json_settings2 import load_settings

    DEBUG = True
    STATIC_URL = '/static/'
    ... LOTS OF OTHERS SETTINGS HERE ...

    SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
    load_settings(globals(), directory=SETTINGS_DIR, depth=3)

Essentially this will tell the function to look for the settings file 
starting in the same directory as ``settings.py`` and if not found, 
look up to 3 levels higher in the directory tree. So let's say the 
path if your ``settings.py`` file is ``/home/user/app/current/code/settings.py``

The ``load_settings`` function will search the following paths for 
``.settings.json``:

* ``/home/user/app/current/code/``
* ``/home/user/app/current/``
* ``/home/user/app/``
* ``/home/user/``

Useful if you want to store your settings outside of the code deployment 
directories, which is often the case.

The ``load_settings`` function takes the following variables:

* current_settings - Dictionary that will be updated with found settings. 
                     Generally you'd pass in ``globals()``.
* filename - Name of json file with settings. Defaults to ``.settings.json``
* directory - Path of the directory where ``filename`` lives. Defaults to ``.``.
* depth - Number of parent directories to scan for ``filename``. Defaults to ``0``.
* store = Store settings into the ``current_settings`` dict. Defaults to ``True``.

If ``store`` is set to ``False`` then the ``current_settings`` dict will not 
be altered.

The function will always return the pythonic representation of what was found 
in the json settings file.

**Note on directory** - By default, the ``directory`` variable above is 
set to ``.`` - meaning current directory. This usually means the directory
where you started the Python interpreter or are running ``manage.py`` from.
This is usually NOT what you want. It's best practice to always set the 
expected directory to avoid troubleshooting headaches.

What Is Used As a Setting?
--------------------------

When calling ``load_settings`` you can include extra data in your json 
settings file that is useful for other puposes in your code but is not 
something you want cluttering your ``django.conf.settings`` object.

Only keys that are stored in all capital letters will be stored
to the ``current_settings`` dict. So if your json settings has options 
that are not all caps, they will only be returned as part of the loaded 
json data.

In other words, say you ``load_settings`` on the following data::

    {
        "SeCreT_Key": "This will not be saved in Django settings.",
        "SECRET_KEY": "This WILL be saved in Django settings.",
        "secret_key": :This will not be saved in Django settings."
    }

Your ``SECRET_KEY`` setting will be set to ``This WILL be saved in Django settings.``

Where To Load Settings?
-----------------------

Normally you can place it at the bottom of the ``settings.py`` file. 
However, there are often times that you need those settings to guide 
the values of other settings.

There is nothing stopping you from loading your json settings from 
anywhere in the process. It's up to you. Just remember that if you 
load your settings and then set a duplicate variable AFTER loading 
the json settings, the duplicate variable will have the final say.

For example::

    $ cat .setting.json
    {
        "STATIC_URL": "/my/cool/static/url/"
    }
    $ cat settings.py
    import os
    from json_settings2 import load_settings

    SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
    load_settings(globals(), directory=SETTINGS_DIR, depth=3)

    DEBUG = True
    STATIC_URL = '/static/'
    ... LOTS OF OTHERS SETTINGS HERE ...

The value of your ``STATIC_URL`` setting will be set to ``/static/`` when 
you might be expecting it to be ``/my/cool/static/url/``. Just a heads up.

Copyright & Warranty
====================
All documentation, libraries, and sample code are
Copyright 2019 Netlandish Inc. <hello@netlandish.com>. The library and
sample code are made available to you under the terms of the BSD license
which is contained in the included file, BSD-LICENSE.


==================
Commercial Support
==================

This software, and lots of other software like it, has been built in support of many of
Netlandish's own projects, and the projects of our clients. We would love to help you
on your next project so get in touch by dropping us a note at hello@netlandish.com.
