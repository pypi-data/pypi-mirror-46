from handytools.settings import HANDYTOOLS_MODELS

for model in HANDYTOOLS_MODELS:
    if model == "TextPhrase":
        from .text_phrase_model import TextPhrase
    if model == "TextImagePhrase":
        from .image_phrase_model import TextImagePhrase
