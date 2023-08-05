from django.contrib import admin

from handytools.settings import HANDYTOOLS_MODELS


for model in HANDYTOOLS_MODELS:
    if model == "TextPhrase":
        from .text_phrase_admin import TextPhraseAdminPanel
        from handytools.models import TextPhrase
        admin.site.register(TextPhrase, TextPhraseAdminPanel)
    if model == "TextImagePhrase":
        from .image_phrase_admin import TextImagePhrasesAdminPanel
        from handytools.models import TextImagePhrase
        admin.site.register(TextImagePhrase, TextImagePhrasesAdminPanel)
