from django.contrib import admin
from easy_select2 import select2_modelform

from handytools.models.PhraseModels import TextImagePhrase, TextPhrase


class TextPhraseAdminPanel(admin.ModelAdmin):
    list_display = ['title', 'phrase_type', 'text']
    search_fields = ['title', 'phrase_type', 'text']
    form = select2_modelform(TextPhrase, attrs={'width': '300px'})


class TextImagePhrasesAdminPanel(admin.ModelAdmin):
    list_display = ['title', 'position']
    search_fields = ['title', 'text', 'position']
    form = select2_modelform(TextImagePhrase, attrs={'width': '300px'})
