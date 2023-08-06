from typing import *

UrlPatterns = List[Any]


def rjango_urls(actual_urlpatterns: UrlPatterns = []):
    """
    Reserved for future use.
    A bit of a skeleton atm, use UrlPatterns Type ATM and standard Django url pattern.

    :param actual_urlpatterns: The urls from your urls.py
    :type actual_urlpatterns: UrlPatterns
    :return: The urls passed downstream to Django.
    :rtype: UrlPatterns
    """
    urls_head = []
    urls_tails = []
    return urls_head + actual_urlpatterns + urls_tails
