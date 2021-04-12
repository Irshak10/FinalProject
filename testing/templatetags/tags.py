from django import template

from testing.models import UserTestCase

register = template.Library()


@register.simple_tag
def number_of_tests(request, user_id):
    number = UserTestCase.objects.filter(user=user_id, complete=False).count()
    return number
