from django import template
import re

from testing.models import UserTestCase

register = template.Library()


@register.simple_tag
def number_of_tests(user_id):
    """
    Returns number of available tests that are not completed for current user.

    @param user_id: id of current user --> int
    @return: number of available tests --> int
    """
    number = UserTestCase.objects.filter(user=user_id, complete=False).count()
    return number


@register.simple_tag
def youtube_video_id(video_url):
    """
    Takes URL for Youtube video and get video id using regular expression.

    @param video_url: copy/paste URL for Youtube video from browser
    @return: unique video id (e.g. Y5d34GhB)
    """
    video_id = re.split('v=|&', video_url)[1]
    return video_id
