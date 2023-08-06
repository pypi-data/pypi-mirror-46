# Django Vegetarian Cookbook, Copyright © 2018 Sergey Panasenko.
# Contacts: <sergey.panasenko@gmail.com>
# License: https://opensource.org/licenses/AGPL-3.0

from django.db import models
from django.utils.translation import gettext_lazy as _
from ajaximage.fields import AjaxImageField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from .translit import transliterate

class Nutrient(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('tag name'))
    def __str__(self):
        return self.name
    class Meta:
        verbose_name=_('nutrient')
        verbose_name_plural=_('nutrients')

class Unit(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('unit name'),
                            help_text=_("Example: cup"))
    plural = models.CharField(max_length=250, blank=True,
            verbose_name=_('plural form'),
            help_text=_("Example: cups (comma separated " +
                            "if language has more 2 plural forms)"))
    def __str__(self):
        return self.name
    class Meta:
        verbose_name=_('unit')
        verbose_name_plural=_('units')

class Ingredient(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('ingredient name'))
    image = models.ImageField(upload_to='images', blank=True,
                                    verbose_name=_('image'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    energy = models.DecimalField(max_digits=7, decimal_places=3, null=True,
                                    blank=True, verbose_name=_('energy'))
    protein = models.DecimalField(max_digits=7, decimal_places=3, null=True,
                                    blank=True, verbose_name=_('protein'))
    fat = models.DecimalField(max_digits=7, decimal_places=3, null=True,
                                    blank=True, verbose_name=_('fat'))
    carbohydrate = models.DecimalField(max_digits=7, decimal_places=3,
                        null=True, blank=True, verbose_name=_('carbohydrate'))
    thumbnail = ImageSpecField(source='image',
          processors=[ResizeToFill(400, 300)],
          format='JPEG',
          options={'quality': 90})
    def __str__(self):
        return self.name
    class Meta:
        verbose_name=_('ingredient')
        verbose_name_plural=_('ingredients')

class IngredientUnit(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT,
                                    verbose_name=_('ingredient'))
    unit = models.ForeignKey(Unit, default=1, on_delete=models.PROTECT,
                                    verbose_name=_('unit'))
    ratio = models.DecimalField(default=1, max_digits=10, decimal_places=4,
                                    verbose_name=_('ratio'))
    def __str__(self):
        return self.ingredient.name + '/' + self.unit.name
    class Meta:
        verbose_name=_('additional unit')
        verbose_name_plural=_('additional units')

class IngredientNutritionalValue(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT,
                                    verbose_name=_('ingredient'))
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE,
                                    verbose_name=_('nutrient'))
    value = models.DecimalField(default=1, max_digits=10, decimal_places=3,
                                    verbose_name=_('value'))
    unit = models.ForeignKey(Unit, default=1, on_delete=models.PROTECT,
                                    verbose_name=_('unit'))
    def __str__(self):
        return self.ingredient.name + '/' + self.nutrient.name
    class Meta:
        verbose_name=_('nutrient')
        verbose_name_plural=_('nutrients')

class Category(models.Model):
    name = models.CharField(max_length=120, verbose_name=_('categoty name'))
    image = models.ImageField(null=True, blank=True, upload_to='images',
                                verbose_name=_('image'))
    thumbnail = ImageSpecField(source='image',
          processors=[ResizeToFill(64, 64)],
          format='png',
          options={'quality': 90})
    def __str__(self):
        return self.name
    class Meta:
        verbose_name=_('category')
        verbose_name_plural=_('categories')

class Tag(models.Model):
    name = models.CharField(max_length=120, verbose_name=_('tag name'))
    counter = models.IntegerField(default=0, verbose_name=_('counter'))
    def __str__(self):
        return self.name
    def weight(self):
        return self.counter
    class Meta:
        verbose_name=_('tag')
        verbose_name_plural=_('tags')

class Recipe(models.Model):
    STATUS_CHOICES = (
        (u'P', _('published')),
        (u'd', _('draft')),
        (u'i', _('idea')),
    )
    COMPLEXITY_CHOICES = (
        (1, _('еasy')),
        (2, _('medium')),
        (3, _('hard')),
    )
    title = models.CharField(max_length=250, unique=True,
                            verbose_name=_('title'))
    url = models.CharField(max_length=250, default='', unique=True, blank=True,
                            verbose_name=_('recipe url'))
    status = models.CharField(max_length=2, default=u'i',
                            choices=STATUS_CHOICES,
                            verbose_name=_('status'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                            verbose_name=_('category'))
    сomplexity = models.IntegerField(default=1, choices=COMPLEXITY_CHOICES,
                            verbose_name=_('сomplexity'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    time = models.IntegerField(default=0, null=True, blank=True,
                            verbose_name=_('time'),
                            help_text=_("Total time for cooking, in minutes"))
    manually_weight = models.IntegerField(default=None, null=True, blank=True,
                            verbose_name=_('weight'),
                            help_text=_("Weight after cooking, in grams"))
    manually_energy = models.DecimalField(default=None, null=True, blank=True,
                            max_digits=7, decimal_places=3,
                            verbose_name=_('energy'))
    manually_protein = models.DecimalField(default=None, null=True, blank=True,
                            max_digits=7, decimal_places=3,
                            verbose_name=_('protein'))
    manually_fat = models.DecimalField(default=None, null=True, blank=True,
                            max_digits=7, decimal_places=3,
                            verbose_name=_('fat'))
    manually_carbohydrate = models.DecimalField(default=None, null=True,
                            blank=True, max_digits=7, decimal_places=3,
                            verbose_name=_('carbohydrate'))
    weight = models.IntegerField(default=0, verbose_name=_('weight'),
                            help_text=_("Weight after cooking, in grams"))
    energy = models.DecimalField(default=0, max_digits=7, decimal_places=3,
                            verbose_name=_('energy'))
    protein = models.DecimalField(default=0, max_digits=7, decimal_places=3,
                            verbose_name=_('protein'))
    fat = models.DecimalField(default=0, max_digits=7, decimal_places=3,
                            verbose_name=_('fat'))
    carbohydrate = models.DecimalField(default=0, max_digits=7,
                            decimal_places=3, verbose_name=_('carbohydrate'))
    image = AjaxImageField(null=True, blank=True, upload_to='images',
                            max_width=1024, max_height=768, crop=True,
                            verbose_name=_('image'))
    thumbnail = ImageSpecField(source='image',
                            processors=[ResizeToFill(400, 300)],
                            format='JPEG', options={'quality': 90})
    tags = models.ManyToManyField(Tag, blank=True,
                            verbose_name=_('tags'), help_text=_('tags'))
    def __str__(self):
        return self.title
    def calculate(self):
        energy = 0
        protein = 0
        fat = 0
        carbohydrate = 0
        weight = 0
        for ingredient in self.recipeingredient_set.all():
            w = ingredient.weight
            weight = weight + w
            if ingredient.ingredient.energy:
                energy += float(ingredient.ingredient.energy) * w / 100
            if ingredient.ingredient.protein:
                protein += ingredient.ingredient.protein * w / 100
            if ingredient.ingredient.fat:
                fat += ingredient.ingredient.fat * w / 100
            if ingredient.ingredient.carbohydrate:
                carbohydrate += ingredient.ingredient.carbohydrate * w / 100
        if self.manually_weight:
            weight = self.manually_weight
        if weight:
            self.energy = float(energy / weight * 100) \
                    if self.manually_energy == None else self.manually_energy
            self.protein = float(protein / weight * 100) \
                    if self.manually_protein == None else self.manually_protein
            self.fat = float(fat / weight * 100) \
                    if self.manually_fat == None else self.manually_fat
            self.carbohydrate = float(carbohydrate / weight * 100) \
                    if self.manually_carbohydrate == None \
                    else self.manually_carbohydrate
            self.weight = weight if self.manually_weight == None \
                    else self.manually_weight
    def count_tags(self):
        for tag in self.tags.all():
            counter = Recipe.objects.filter(models.Q(tags__name=tag.name),
                                            status=u'P').count()
            tag = Tag.objects.get(id = tag.id)
            tag.counter = counter
            tag.save()
    def fullness(self):
        fullness = 0
        if (self.image):
            fullness = fullness + 20
        if (len(self.description)):
            fullness = fullness + 10
        ok_gram = True
        ok_energy = True
        ok_energy = True
        if (len(self.recipeingredient_set.all())):
            fullness = fullness + 20
            for ingredient in self.recipeingredient_set.all():
                if ingredient.roughly:
                    ok_gram = False
                if ingredient.ingredient.energy == None:
                    ok_energy = False
                if ingredient.ingredient.protein == None or \
                        ingredient.ingredient.fat == None or \
                        ingredient.ingredient.carbohydrate == None:
                    ok_nutrients = False
            if (ok_gram):
                fullness = fullness + 20
            if (ok_energy):
                fullness = fullness + 20
            if (ok_energy):
                fullness = fullness + 5
        if (len(self.recipeimage_set.all())):
            fullness = fullness + 5
        return '%i%%' % fullness
    fullness.short_description = _('fullness')
    def recipe_tags(self):
        return ", ".join([t.name for t in self.tags.all()])
    recipe_tags.short_description = _('tags')
    def recipe_ingredients(self, maximum = 3, weight = False, more = False):
        ingredients = []
        for i in self.recipeingredient_set.all():
            ingredients.append(i.ingredient.name + ((': ' + str(i.weight) + \
                                ' ' + str(_('gr'))) if weight else ''))
        return ', '.join(ingredients[0:maximum]) + \
                    (' ...' if (maximum < len(ingredients) and more) else '')
    recipe_ingredients.short_description = _('ingredients')
    def fix_url(self):
        self.url = transliterate(self.title)
    def has_roughly(self):
        hr = False
        for i in self.recipeingredient_set.all():
            if (i.roughly):
                hr = True
        return hr
    has_roughly.short_description = _('Has roughly')
    class Meta:
        verbose_name=_('recipe')
        verbose_name_plural=_('recipes')


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                                verbose_name=_('recipe'))
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                verbose_name=_('ingredient'))
    weight = models.IntegerField(default=0, null=True, blank=True,
                                verbose_name=_('weight in gram'))
    quantity = models.DecimalField(max_digits=4, decimal_places=2, default=0,
                                verbose_name=_('quantity on additional unit'))
    unit = models.ForeignKey(Unit, default=None, null=True, blank=True,
                                on_delete=models.CASCADE,
                                verbose_name=_('additional unit'))
    roughly = models.BooleanField(default=False, verbose_name=_('roughly'))
    def __str__(self):
        return self.ingredient.name
    class Meta:
        verbose_name=_('ingredient')
        verbose_name_plural=_('ingredients')

class RecipeImage(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                                verbose_name=_('recipe'))
    image = AjaxImageField(null=True, blank=True, upload_to='images',
                                max_width=1024, max_height=768, crop=True,
                                verbose_name=_('image'))
    thumbnail = ImageSpecField(source='image',
                                processors=[ResizeToFill(400, 300)],
                                format='JPEG', options={'quality': 90})
    title = models.CharField(max_length=250, blank=True,
                                verbose_name=_('title'))
    def __str__(self):
        return _('image') + '-' + str(self.id)
    class Meta:
        verbose_name=_('image')
        verbose_name_plural=_('images')


