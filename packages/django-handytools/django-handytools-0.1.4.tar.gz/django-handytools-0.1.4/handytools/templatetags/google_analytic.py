from django import template

register = template.Library()


@register.inclusion_tag("handytools/google-analytics.html")
def google_analytic(api_key):
    return {
        "api_key": api_key
    }
