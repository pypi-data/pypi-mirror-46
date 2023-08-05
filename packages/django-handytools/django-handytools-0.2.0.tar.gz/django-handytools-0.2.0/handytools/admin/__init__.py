from django.contrib import admin

from handytools.settings import HANDYTOOLS_MODELS

from .PhraseModelsAdmin import TextImagePhrasesAdminPanel, TextPhraseAdminPanel

for model in HANDYTOOLS_MODELS:
    if model == "TextPhrase":
        from handytools.models.PhraseModels import TextPhrase
        admin.site.register(TextPhrase, TextPhraseAdminPanel)
    if model == "TextImagePhrase":
        from handytools.models.PhraseModels import TextImagePhrase
        admin.site.register(TextImagePhrase, TextImagePhrasesAdminPanel)
