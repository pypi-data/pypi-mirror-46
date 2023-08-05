from django import forms
from easy_select2.widgets import Select2

from handytools.models import TextImagePhrase
from handytools.settings import TEXT_IMAGE_PHRASE_MODEL_POSITIONS


class TextImagePhraseForm(forms.ModelForm):
    position = forms.ChoiceField(
        choices=TEXT_IMAGE_PHRASE_MODEL_POSITIONS, widget=Select2())

    class Meta:
        model = TextImagePhrase
        fields = '__all__'
