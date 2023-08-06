from django.conf import settings

HANDYTOOLS_MODELS = getattr(settings, "HANDYTOOLS_MODELS", [])

TEXT_PHRASE_MODEL_PHRASE_TYPES = getattr(
    settings, "TEXT_PHRASE_MODEL_PHRASES_TYPES", [])

TEXT_IMAGE_PHRASE_MODEL_POSITIONS = getattr(
    settings, "TEXT_IMAGE_PHRASE_MODEL_POSITIONS", [])

TEXT_PHRASE_SIMPLE_CONTEXT_OBJECT_NAME = getattr(
    settings, "TEXT_PHRASE_SIMPLE_CONTEXT_OBJECT_NAME", "text_phrases")

TEXT_PHRASE_LANG_CONTEXT_OBJECT_NAME = getattr(
    settings, "TEXT_PHRASE_LANG_CONTEXT_OBJECT_NAME", "text_phrases_lang")


def _get_languages():
    """
    generate language list with Global Key
    for language independent phrases
    """
    language_list = [
        ("global", 'Global')
    ]
    for item in getattr(settings, "LANGUAGES", []):
        language_list.append(item)
    return language_list


TEXT_PHRASE_LANGUAGES = _get_languages
