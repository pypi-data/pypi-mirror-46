from django.contrib import admin

from .forms import TextImagePhraseForm
from .models import TextImagePhrase


class TextImagePhrasesAdminPanel(admin.ModelAdmin):
    list_display = ['title', 'position']
    search_fields = ['title', 'text', 'position']
    form = TextImagePhraseForm


admin.site.register(TextImagePhrase, TextImagePhrasesAdminPanel)
