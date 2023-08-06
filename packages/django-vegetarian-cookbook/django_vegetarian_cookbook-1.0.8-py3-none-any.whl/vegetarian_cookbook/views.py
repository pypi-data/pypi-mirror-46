# Django Vegetarian Cookbook, Copyright © 2018 Sergey Panasenko.
# Contacts: <sergey.panasenko@gmail.com>
# License: https://opensource.org/licenses/AGPL-3.0

import math
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import Context
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

from vegetarian_cookbook import appsettings
from vegetarian_cookbook.models import Recipe, Category, Tag, Ingredient

def index(request, page = 1):
    recipes_list = Recipe.objects.all().filter(status=u'P').order_by('-id')
    try:
        paginator = Paginator(recipes_list, appsettings.RECIPES_IN_LIST)
        recipes = paginator.page(page)
    except PageNotAnInteger:
        recipes = paginator.page(1)
    except EmptyPage:
        raise Http404("Not correct page number")
    recipes.base_url = ''
    return render(request, 'vegetarian_cookbook/list.html', {
        'recipes': recipes,
        'title': _('All recipes'),
        'seo_description': appsettings.SEO_DESCRIPTION,
        'seo_keywords': appsettings.SEO_KEYWORDS,
    })

def detail(request, recipe_name):
    try:
        if request.user.has_perm('vegetarian_cookbook.change_recipe'):
            # admin can see drafts and ideas, users only published
            recipe = Recipe.objects.get(url=recipe_name)
        else:
            recipe = Recipe.objects.get(url=recipe_name, status=u'P')
    except Recipe.DoesNotExist:
        raise Http404("Recipe does not exist")
    return render(request, 'vegetarian_cookbook/detail.html', {
        'recipe': recipe,
        'seo_description': recipe.recipe_ingredients(20, False, True),
        'seo_keywords': recipe.recipe_tags() + ', ' + appsettings.SEO_KEYWORDS,
    })

def tags(request, tags, page = 1):
    tags_list = tags.split(",");
    recipes_list = Recipe.objects.all().filter(Q(tags__name__in=tags_list),
                                status=u'P').distinct().order_by('-id')
    try:
        paginator = Paginator(recipes_list, appsettings.RECIPES_IN_LIST)
        recipes = paginator.page(page)
    except PageNotAnInteger:
        recipes = paginator.page(1)
    except EmptyPage:
        recipes = paginator.page(paginator.num_pages)
    recipes.base_url = reverse('recipes_tags', args=[tags])
    return render(request, 'vegetarian_cookbook/list.html', {
        'recipes': recipes,
        'title': _('Tags: %(tags)s.') % {'tags': tags},
        'seo_description': appsettings.SEO_DESCRIPTION + \
                        _('Tags: %(tags)s.') % {'tags': tags} ,
        'seo_keywords': tags + ', ' + appsettings.SEO_KEYWORDS,
    })


def category(request, category_name, page = 1):
    try:
        category = Category.objects.get(name=category_name)
        recipes_list = Recipe.objects.filter(category=category.id,
                                        status=u'P').order_by('-id')
        paginator = Paginator(recipes_list, appsettings.RECIPES_IN_LIST)
        recipes = paginator.page(page)
    except PageNotAnInteger:
        recipes = paginator.page(1)
    except EmptyPage:
        recipes = paginator.page(paginator.num_pages)
    except Category.DoesNotExist:
        raise Http404("Category does not exist")
    recipes.base_url = reverse('recipes_category', args=[category_name])
    return render(request, 'vegetarian_cookbook/list.html', {
        'recipes': recipes,
        'title': _('Category: %(category)s.') % {'category': category.name},
        'seo_description': appsettings.SEO_DESCRIPTION + \
         _('Category: %(category)s.') % {'category': category.name},
        'seo_keywords': category_name + ', ' + appsettings.SEO_KEYWORDS,
    })

def ingredient(request, ingredient_name):
    try:
        ingredient = Ingredient.objects.get(name=ingredient_name)
        recipes = Recipe.objects.all().filter(
                Q(recipeingredient__ingredient__id=ingredient.id), status=u'P')
    except Recipe.DoesNotExist:
        raise Http404("Ingredient does not exist")
    return render(request, 'vegetarian_cookbook/ingredient.html', {
        'ingredient': ingredient,
        'recipes': recipes,
        'seo_description': appsettings.SEO_DESCRIPTION + ingredient_name,
        'seo_keywords': ingredient_name + ', ' + appsettings.SEO_KEYWORDS,
    })

def tags_ingredients(request, page = 1):
    tags = Tag.objects.all()
    search = request.POST.get('search', '')
    ingredients_list = Ingredient.objects.all()
    if search !='':
        ingredients_list = ingredients_list.filter(name__icontains=search)
    try:
        paginator = Paginator(ingredients_list.order_by('name'),
                                appsettings.INGREDIENTS_IN_LIST)
        ingredients = paginator.page(page)
    except PageNotAnInteger:
        ingredients = paginator.page(1)
    except EmptyPage:
        ingredients = paginator.page(paginator.num_pages)
    ingredients.base_url = reverse('recipe_tags_ingredients')
    return render(request, 'vegetarian_cookbook/tags_ingredients.html', {
        'tags': tags,
        'search':search,
        'ingredients': ingredients,
        'title': _("Tags & Ingredients"),
        'seo_description': appsettings.SEO_DESCRIPTION,
        'seo_keywords': appsettings.SEO_KEYWORDS,
    })

def search(request):
    search = {
        'categories': Category.objects.all(),
        'сomplexity_choices':[],
        'energy': {
            'min': math.floor(Recipe.objects.filter(status=u'P') \
                    .order_by('energy')[0].energy),
            'max': math.ceil(Recipe.objects.filter(status=u'P') \
                    .order_by('-energy')[0].energy),
            },
        'time': {
            'min': int(Recipe.objects.filter(status=u'P').exclude(time=0) \
                    .order_by('time')[0].time),
            'max': int(Recipe.objects.filter(status=u'P').exclude(time=0) \
                    .order_by('-time')[0].time),
            },
        'protein': {
            'min': math.floor(Recipe.objects.filter(status=u'P') \
                    .order_by('protein')[0].protein),
            'max': math.ceil(Recipe.objects.filter(status=u'P') \
                    .order_by('-protein')[0].protein),
            },
        'fat': {
            'min': math.floor(Recipe.objects.filter(status=u'P') \
                    .order_by('fat')[0].fat),
            'max': math.ceil(Recipe.objects.filter(status=u'P') \
                    .order_by('-fat')[0].fat),
            },
        'carbohydrate': {
            'min': math.floor(Recipe.objects.filter(status=u'P') \
                    .order_by('carbohydrate')[0].carbohydrate),
            'max': math.ceil(Recipe.objects.filter(status=u'P') \
                    .order_by('-carbohydrate')[0].carbohydrate),
            },
        'query': request.POST.get('query','').lower(),
        'in_name': request.POST.get('in_name', False),
        'in_ingredient': request.POST.get('in_ingredient', False),
        'in_tag': request.POST.get('in_tag', False),
        'post':repr(request.POST),
    }
    for category in search['categories']:
        category.checked = False
        if request.POST.get('category-%i' % category.id, False):
            category.checked = True
    for key, value in Recipe.COMPLEXITY_CHOICES:
        checked = False
        if request.POST.get('сomplexity-%i' % key, False):
            checked = True
        search['сomplexity_choices'].append({
                'id':key,
                'name':value,
                'checked': checked
                });

    for value in ['energy', 'time', 'protein', 'fat', 'carbohydrate']:
        search[value]['cmin'] = int(request.POST.get(value + '_min',
                                    search[value]['min']))
        search[value]['cmax'] = int(request.POST.get(value + '_max',
                                                search[value]['max']))
    result = {}
    r = Recipe.objects.all()
    if search['query'] != '':
        # by recipe name
        qn = Q(title__icontains=search['query'])
        # by ingridient name
        qi = Q(recipeingredient__ingredient__name__icontains=search['query'])
        # by tag name
        qt = Q(tags__name__icontains=search['query'])
        q = False
        all_empty = not search['in_name'] and \
                    not search['in_ingredient'] and \
                    not search['in_tag']
        if search['in_name'] or all_empty:
            q = qn
        if search['in_ingredient'] or all_empty:
            q = qi if q == False else q | qi
        if search['in_tag'] or all_empty:
            q = qt if q == False else q | qt
        if q != False:
            r = r.filter(q)

    # search in some categories
    q = False
    for category in search['categories']:
        if category.checked:
            qq = Q(category=category)
            q = qq if q == False else q | qq
    if q != False:
        r = r.filter(q)

    # by сomplexity
    q = False
    for сomplexity in search['сomplexity_choices']:
        if сomplexity['checked']:
            qq = Q(сomplexity=сomplexity['id'])
            q = qq if q == False else q | qq
    if q != False:
        r = r.filter(q)

    # by energy
    if search['energy']['cmin'] != search['energy']['min']:
        r = r.filter(energy__gte = search['energy']['cmin'])
    if search['energy']['cmax'] != search['energy']['max']:
        r = r.filter(energy__lte = search['energy']['cmax'])

    # by time
    if search['time']['cmin'] != search['time']['min']:
        r = r.filter(time__gte = search['time']['cmin'])
    if search['time']['cmax'] != search['time']['max']:
        r = r.filter(time__lte = search['time']['cmax'])

    # by protein
    if search['protein']['cmin'] != search['protein']['min']:
        r = r.filter(protein__gte = search['protein']['cmin'])
    if search['protein']['cmax'] != search['protein']['max']:
        r = r.filter(protein__lte = search['protein']['cmax'])

    # by fat
    if search['fat']['cmin'] != search['fat']['min']:
        r = r.filter(fat__gte = search['fat']['cmin'])
    if search['fat']['cmax'] != search['fat']['max']:
        r = r.filter(fat__lte = search['fat']['cmax'])

    # by carbohydrate
    if search['carbohydrate']['cmin'] != search['carbohydrate']['min']:
        r = r.filter(carbohydrate__gte = search['carbohydrate']['cmin'])
    if search['carbohydrate']['cmax'] != search['carbohydrate']['max']:
        r = r.filter(carbohydrate__lte = search['carbohydrate']['cmax'])

    result["recipes"] = r.filter(status=u'P').distinct().order_by('-id')
    return render(request, 'vegetarian_cookbook/search.html', {
        'search': search,
        'result': result,
        'title': _("Search"),
        'seo_description': appsettings.SEO_DESCRIPTION,
        'seo_keywords': appsettings.SEO_KEYWORDS,
    })

def robots(request):
    r = render_to_string('vegetarian_cookbook/robots.txt', {
        'url': request.build_absolute_uri().replace('/robots.txt',''),
    })
    return HttpResponse(r, content_type="text/plain; charset=utf-8")

def sitemap(request):
    recipes = Recipe.objects.all().filter(status=u'P').order_by('-id')
    sm = render_to_string('vegetarian_cookbook/sitemap.xml', {
        'recipes': recipes,
        'url': request.build_absolute_uri().replace('/sitemap.xml',''),
    })
    return HttpResponse(sm, content_type="text/xml; charset=utf-8")
