
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.translation import gettext_lazy as _
from filer.fields.image import FilerImageField


class TextImagePhraseAbstractModel(models.Model):
    """
    we use those fields in other abstract models.
    """
    title = models.CharField(
        max_length=255,
        verbose_name=_('Title')
    )
    image = FilerImageField(
        verbose_name=_('Image'),
        on_delete=models.CASCADE
    )
    text = RichTextUploadingField(
        verbose_name=_('Text')
    )
    position = models.CharField(max_length=255, verbose_name=_('Location'))

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        abstract = True
        verbose_name = _('Text & Image Phrase')
        verbose_name_plural = _('Text & Image Phrases')


class TextImagePhrase(TextImagePhraseAbstractModel):
    """
    this model will implement TextImagePhraseAbstractModel.
    if you don't like style or fields you can import
    TextImagePhraseAbstractModel and overwrite this model,
    and then delete TextImagePhraseModel from settings.py
    """
