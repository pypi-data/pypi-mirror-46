from django import template

register = template.Library()


@register.inclusion_tag("handyutils/google-analytics.html")
def google_analytic(api_key=None):
    if not api_key:
        raise Exception("google api key is required.")
    return {
        "api_key": api_key
    }
