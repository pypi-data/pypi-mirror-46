from django.contrib import admin
from easy_select2 import select2_modelform

from handytools.models.PhraseModels import TextPhrase


class TextPhraseAdminPanel(admin.ModelAdmin):
    list_display = ['phrase_type', 'text']
    search_fields = ['phrase_type', 'text']
    form = select2_modelform(TextPhrase, attrs={'width': '300px'})
