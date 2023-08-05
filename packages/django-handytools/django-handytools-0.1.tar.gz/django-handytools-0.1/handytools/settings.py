from django.conf import settings

HANDYTOOLS_MODELS = getattr(settings, "HANDYTOOLS_MODELS", None)

TEXT_PHRASE_MODEL_PHRASE_TYPES = getattr(
    settings, "TEXT_PHRASE_MODEL_PHRASES_TYPES", None)


def get_languages():
    """
    will generate language list with Global Key
    for language independent phrases
    """
    language_list = [
        ("global", 'Global')
    ]
    for item in getattr(settings, "LANGUAGES", None):
        language_list.append(item)
    return language_list


TEXT_PHRASE_LANGUAGES = get_languages
