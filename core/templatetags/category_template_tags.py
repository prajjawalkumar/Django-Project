from django import template
from django.utils.safestring import mark_safe

from core.models import Category

register = template.Library()


from core.models import Category

register = template.Library()

SALE_CATEGORY_SLUGS = [
    'top-deals', 'mens-sale', 'womens-sale', 'footwear-sale', 
    'accesories-sale', 'summer-sale', 'combo-offers', 
    'best-sellers', 'under-499', 'under-699', 'winter-sale'
]

@register.simple_tag
def categories():
    items = Category.objects.filter(is_active=True, parent=None).exclude(slug__in=SALE_CATEGORY_SLUGS).order_by('title')
    items_li = ""
    for i in items:
        items_li += """<li><a href="/category/{}">{}</a></li>""".format(i.slug, i.title)
    return mark_safe(items_li)

@register.simple_tag
def categories_mobile():
    items = Category.objects.filter(is_active=True, parent=None).exclude(slug__in=SALE_CATEGORY_SLUGS).order_by('title')
    items_li = ""
    for i in items:
        items_li += """<li class="item-menu-mobile"><a href="/category/{}">{}</a></li>""".format(i.slug, i.title)
    return mark_safe(items_li)

@register.simple_tag
def categories_li_a():
    items = Category.objects.filter(is_active=True, parent=None).exclude(slug__in=SALE_CATEGORY_SLUGS).order_by('title')
    items_li_a = ""
    for i in items:
        items_li_a += """<li class="p-t-4"><a href="/category/{}" class="s-text13">{}</a></li>""".format(i.slug, i.title)
    return mark_safe(items_li_a)

@register.simple_tag
def sale_categories():
    return Category.objects.filter(slug__in=SALE_CATEGORY_SLUGS).order_by('id')

@register.simple_tag
def categories_div():
    items = Category.objects.filter(is_active=True, parent=None).exclude(slug__in=SALE_CATEGORY_SLUGS).order_by('title')
    # ... (rest of the code remains the same but using the filtered items)
    items_div = ""
    item_div_list = ""
    for i, j in enumerate(items):
        if not i % 2:
            items_div += """<div class="block1 hov-img-zoom pos-relative m-b-30"><img src="/media/{}" alt="IMG-BENNER"><div class="block1-wrapbtn w-size2"><a href="/category/{}" class="flex-c-m size2 m-text2 bg3 hov1 trans-0-4">{}</a></div></div>""".format(
                j.image, j.slug, j.title)
        else:
            items_div_ = """<div class="block1 hov-img-zoom pos-relative m-b-30"><img src="/media/{}" alt="IMG-BENNER"><div class="block1-wrapbtn w-size2"><a href="/category/{}" class="flex-c-m size2 m-text2 bg3 hov1 trans-0-4">{}</a></div></div>""".format(
                j.image, j.slug, j.title)
            item_div_list += """<div class="col-sm-10 col-md-8 col-lg-4 m-l-r-auto">""" + items_div + items_div_ + """</div>"""
            items_div = ""

    return mark_safe(item_div_list)
