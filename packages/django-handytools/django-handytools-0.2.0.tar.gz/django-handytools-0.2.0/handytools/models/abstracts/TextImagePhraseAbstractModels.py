from django.db import models
from django.utils.translation import gettext_lazy as _

from handytools.settings import TEXT_IMAGE_PHRASE_MODEL_PHRASE_TYPES

from .PublicFields import PublicFields


class TextImagePhraseAbstractModel(PublicFields):
    position = models.CharField(
        max_length=255,
        choices=TEXT_IMAGE_PHRASE_MODEL_PHRASE_TYPES,
        verbose_name=_('Location'),
    )

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        abstract = True
        verbose_name = _('Text & Image Phrase')
        verbose_name_plural = _('Text & Image Phrases')
