*********************
django-script-pattern
*********************

This app allows you to add ``script`` blocks into your pages using url patterns like:
    
- /category/*
- /\*/subcategory/\*

# Includes GET parameters

- /products/catalog/\*category=some-category\*
    

Use ``*`` to pass any symbols and ``$`` as the end. 

Available to use four block locations:

1. Head - Top
2. Head - Bottom
3. Body - Top
4. Body - Bottom

************
Installation
************

Install with pip:

.. code:: shell

    $ pip install django-script-pattern


**********************
Update INSTALLED_APPS:
**********************

.. code:: python

    INSTALLED_APPS = [
        ...
        'script_pattern',
        'django-admin-sortable2',
        'django_jinja',  # optional for jinja2 global function
        ...
    ]

Apply migrations:

.. code:: shell

    $ python manage.py migrate

---------------
Example to use:
---------------

.. code:: jinja

    #layout.jinja
    <html lang="en">
        <head>
            {{ get_script_pattern(request, 'head', 'top') }}
            ...
            some head content
            ...
            {{ get_script_pattern(request, 'head', 'bottom') }}
        </head>

        <body>
            {{ get_script_pattern(request, 'body', 'top') }}
            ...
            some body content
            ...
            {{ get_script_pattern(request, 'body', 'bottom') }}
        </body>
    </html>