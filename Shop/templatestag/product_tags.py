from django import template
from ..models import *

tag = template.Library()

@tag.simple_tag()
def get_tag():
    return Tag.objects.filter(in_stock = True)


@tag.simple_tag()
def get_category():
    return Category.objects.filter(in_stock = True)


@tag.simple_tag()
def get_brand():
    return Brand.objects.filter(in_stock = True)