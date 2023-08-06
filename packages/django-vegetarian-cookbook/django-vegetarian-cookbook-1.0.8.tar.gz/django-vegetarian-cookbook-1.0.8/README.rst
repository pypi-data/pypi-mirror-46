##############################
Django Vegetarian Cookbook
##############################


Django application for the publication of vegetarian culinary recipes with the calculation of energy and nutrients.

********
Features
********

* manage ingridients, include ingridient nutrients and energy
* manage additional meashures
* manage recipes
* recipe category
* recipe tag
* show recipe
* calculate recipe energy
* search recipes by many parameters


************
Installation
************

pip install django-vegetarian-cookbook

add apps in settings.py

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'vegetarian_cookbook',
        'bootstrap4',
        'ajaximage',
        'imagekit',
        'ckeditor',
    ]

add url in urls.py

.. code-block:: python

    from django.conf.urls import include

    urlpatterns = [
        path('', include('vegetarian_cookbook.urls')),
        path('admin/', admin.site.urls),
    ]

more info see in example app

https://github.com/sergey-panasenko/django-vegetarian-cookbook
