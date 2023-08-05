from handytools.settings import HANDYTOOLS_MODELS

for model in HANDYTOOLS_MODELS:
    if model == "TextPhrase":
        from .text_phrase_form import TextPhraseForm
    if model == "TextImagePhrase":
        from .image_phrase_form import TextImagePhraseForm
