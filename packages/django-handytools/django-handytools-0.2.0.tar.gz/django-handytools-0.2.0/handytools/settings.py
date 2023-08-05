from django.conf import settings

HANDYTOOLS_MODELS = getattr(settings, "HANDYTOOLS_MODELS", None)

TEXT_PHRASE_MODEL_PHRASE_TYPES = getattr(
    settings, "TEXT_PHRASE_MODEL_PHRASES_TYPES", None)

TEXT_IMAGE_PHRASE_MODEL_PHRASE_TYPES = getattr(
    settings, "TEXT_IMAGE_PHRASE_MODEL_PHRASE_TYPES", None)

TEXT_PHRASE_SIMPLE_CONTEXT_OBJECT_NAME = getattr(
    settings, "TEXT_PHRASE_SIMPLE_CONTEXT_OBJECT_NAME", "text_phrases")

TEXT_PHRASE_LANG_CONTEXT_OBJECT_NAME = getattr(
    settings, "TEXT_PHRASE_LANG_CONTEXT_OBJECT_NAME", "text_phrases_lang")


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
