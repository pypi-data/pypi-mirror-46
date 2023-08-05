from django.db import models
from django.utils.translation import gettext_lazy as _

from handytools.settings import (TEXT_PHRASE_LANGUAGES,
                                 TEXT_PHRASE_MODEL_PHRASE_TYPES,)


class TextPhrase(models.Model):
    """
    use this model for phrases that have text in it, not image
    like email, phone, location, copyright note, releated links,
     social network links, languages.
     text field length is limited to 2000 character
     you can add multiple text phrase with the same phrase type.
     example:
        phrase_type : text
        ------------------
        LANGUAGE    : en
        LANGUAGE    : fr
     """

    phrase_type = models.CharField(
        null=False,
        blank=False,
        db_index=True,
        max_length=255,
        choices=TEXT_PHRASE_MODEL_PHRASE_TYPES,
        verbose_name=_('Phrase Type')
    )
    text = models.TextField(
        null=False,
        blank=False,
        verbose_name=_('Text')
    )
    language = models.CharField(
        null=False, blank=False, default="global", max_length=6,
        choices=TEXT_PHRASE_LANGUAGES(), verbose_name=_('Language')
    )

    def __str__(self):
        return self.phrase_type

    def __unicode__(self):
        return u'%s' % self.phrase_type

    class Meta:
        ordering = ('phrase_type',)
        verbose_name = _('Text Phrase')
        verbose_name_plural = _('Text Phrases')
