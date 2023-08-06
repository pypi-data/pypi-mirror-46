from django.utils.translation import gettext as _
from django.conf import settings

RECIPES_IN_LIST = 6
INGREDIENTS_IN_LIST = 20
SEO_DESCRIPTION = _('The best proven vegetarian recipes with ' + \
                         'calculation of calories and nutrients.')
SEO_KEYWORDS = _('recipe, culinary, cookbook, vegetarian food, vegan,' + \
                  'raw food, raw diet, vegetarianism, diet, healthy food,')
NPLURALS = 2
PLURAL = '0 if n==1 else 1'

# load varitables from settings
for v in list(vars().keys()):
    if v[:1] != '_' and v.upper() == v:
        newv = getattr(settings, v, None)
        if newv != None:
            statement = str(v) + " = " + str(newv)
            if isinstance(newv, str):
                statement = str(v) + " = '" + str(newv) + "'"
            exec(statement)
