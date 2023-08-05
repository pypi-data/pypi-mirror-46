from handytools.models.abstracts.TextImagePhraseAbstractModels import \
    TextImagePhraseAbstractModel
from handytools.models.abstracts.TextPhraseAbstractModels import \
    TextPhraseAbstractModel


class TextPhrase(TextPhraseAbstractModel):
    """
    this model will implement TextPhraseAbstractModel.
    if you don't like style or fields you can import
    TextPhraseAbstractModel and overwrite this model,
    and then delete TextPhraseModel from settings.py.
    use this model for phrases that have text in it, not images
    like email, phone, location, copyright note, releated links,
    social network links, languages.
    text field length is limited to 2000 character
    you can add multiple text phrase with the same phrase type.
    example:
        title : phrase_type : text
        --------------------------
        copyright    : copyright    : 2018
        AboutUsFr    : aboutus      : AboutUs
        facebook url : facebook_url : https://facebook.com
    """


class TextImagePhrase(TextImagePhraseAbstractModel):
    """
    this model will implement TextImagePhraseAbstractModel.
    if you don't like style or fields you can import
    TextImagePhraseAbstractModel and overwrite this model,
    and then delete TextImagePhraseModel from settings.py
    """
