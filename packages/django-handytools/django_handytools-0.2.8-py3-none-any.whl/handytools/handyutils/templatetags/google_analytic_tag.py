from django import template

register = template.Library()


@register.inclusion_tag("handyutils/google-analytics.html")
def google_analytic(api_key=None):
    if not api_key:
        raise Exception("Please send google api key to google_analytic tag")
    return {
        "api_key": api_key
    }
