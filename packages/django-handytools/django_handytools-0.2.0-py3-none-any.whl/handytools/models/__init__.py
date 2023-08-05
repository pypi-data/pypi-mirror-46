import importlib

from handytools.settings import HANDYTOOLS_MODELS

for model in HANDYTOOLS_MODELS:
    if model == "TextPhrase":
        from .PhraseModels import TextPhrase
    if model == "TextImagePhrase":
        from .PhraseModels import TextImagePhrase
