from django.contrib import admin

from .forms import TextImagePhraseForm


class TextImagePhrasesAdminPanel(admin.ModelAdmin):
    list_display = ['title', 'position']
    search_fields = ['title', 'text', 'position']
    form = TextImagePhraseForm
