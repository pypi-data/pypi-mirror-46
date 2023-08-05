from handytools.models.PhraseModels import TextPhrase


def text_phrase_simple_cp(request):
    text_phrases = TextPhrase.objects.all()
    return {
        'text_phrases': text_phrases
    }


def text_phrase_language_cp(request):
    """
    will filter the phrases base on current language
    """
    text_phrases = TextPhrase.objects.filter(language=request.LANGUAGE_CODE)
    return {
        'text_phrases': text_phrases
    }
