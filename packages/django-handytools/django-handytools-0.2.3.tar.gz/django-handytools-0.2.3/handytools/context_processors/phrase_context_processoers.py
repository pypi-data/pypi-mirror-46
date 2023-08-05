from handytools.models import TextPhrase
from handytools.settings import (TEXT_PHRASE_LANG_CONTEXT_OBJECT_NAME,
                                 TEXT_PHRASE_SIMPLE_CONTEXT_OBJECT_NAME,)


def text_phrase_simple_cp(request):
    text_phrases = TextPhrase.objects.all()
    return {
        TEXT_PHRASE_SIMPLE_CONTEXT_OBJECT_NAME: text_phrases
    }


def text_phrase_language_cp(request):
    """
    will filter the phrases base on current language
    """
    text_phrases = TextPhrase.objects.filter(language=request.LANGUAGE_CODE)
    return {
        TEXT_PHRASE_LANG_CONTEXT_OBJECT_NAME: text_phrases
    }
