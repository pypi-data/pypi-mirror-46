from django import forms
from easy_select2.widgets import Select2

from handytools.settings import TEXT_IMAGE_PHRASE_MODEL_POSITIONS
from handytools.textimagephrase.models import TextImagePhrase


class TextImagePhraseForm(forms.ModelForm):
    position = forms.ChoiceField(
        choices=TEXT_IMAGE_PHRASE_MODEL_POSITIONS, widget=Select2())

    class Meta:
        model = TextImagePhrase
        fields = '__all__'
