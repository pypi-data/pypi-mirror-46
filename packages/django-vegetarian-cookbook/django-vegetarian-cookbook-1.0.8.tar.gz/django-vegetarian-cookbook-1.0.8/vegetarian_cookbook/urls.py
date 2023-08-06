# Django Vegetarian Cookbook, Copyright © 2018 Sergey Panasenko.
# Contacts: <sergey.panasenko@gmail.com>
# License: https://opensource.org/licenses/AGPL-3.0

from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views

admin.autodiscover()

urlpatterns = [
    re_path(r'^category/(?P<category_name>[\s\w_\-0-9]+)$',
            views.category, name='recipes_category'),
    re_path(r'^category/(?P<category_name>[\s\w_\-0-9]+)/(?P<page>\d+)/$',
            views.category, name='recipes_category_page'),
    re_path(r'^tags/(?P<tags>[\s\w\,_\-0-9]+)$',
            views.tags, name='recipes_tags'),
    re_path(r'^tags/(?P<tags>[\s\w\,_\-0-9]+)/(?P<page>\d+)/$',
            views.tags, name='recipes_tags_page'),
    re_path(r'^recipe/(?P<recipe_name>[A-Za-z_\-0-9]+)$',
            views.detail, name='recipes_recipe'),
    re_path(r'^ingredient/(?P<ingredient_name>[\s\w_\-0-9%\(\)]+)$',
            views.ingredient, name='recipes_ingredient'),
    path('tags-ingredients', views.tags_ingredients,
            name='recipe_tags_ingredients'),
    re_path(r'^tags-ingredients/(?P<page>\d+)/$', views.tags_ingredients,
            name='recipe_tags_ingredients_page'),
    path('search/', views.search, name='recipes_search'),
    path('robots.txt', views.robots, name='robots'),
    path('sitemap.xml', views.sitemap, name='sitemap'),
    path('ajaximage/', include('ajaximage.urls')),
    re_path(r'^(?P<page>\d+)/$', views.index, name='recipes_index_page'),
    path('', views.index, name='recipes_index'),
]
