from django import template

from ..models import PersonPost

register = template.Library()

@register.simple_tag
def person_post_info(person, post):
    return PersonPost.objects.get(person=person, post=post)
