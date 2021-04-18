from django import template
import re

from testing.models import UserTestCase

register = template.Library()


@register.simple_tag
def number_of_tests(user_id):
    number = UserTestCase.objects.filter(user=user_id, complete=False).count()
    return number


@register.simple_tag
def youtube_video_id(video_url):
    video_id = re.split('v=|&', video_url)[1]
    return video_id
