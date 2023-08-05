from django.db import models
from django.utils.translation import gettext_lazy as _

from .public_fields import PublicFields


class TextPhraseAbstractModel(models.Model):
    """
    this is TextPhrase Abstract Model
    if you don't like fields or style of TextPhrase Model you can
    import this abstract model and overwrite it
    """
    title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name=_('Title')
    )
    phrase_type = models.CharField(
        db_index=True,
        max_length=255,
        verbose_name=_('Phrase Type')
    )
    text = models.TextField(
        verbose_name=_('Text')
    )
    language = models.CharField(
        default="global", max_length=6,
        verbose_name=_('Language')
    )

    def __str__(self):
        return self.title or self.phrase_type

    def __unicode__(self):
        return u'%s' % (self.title or self.phrase_type)

    class Meta:
        abstract = True
        ordering = ('phrase_type',)
        verbose_name = _('Text Phrase')
        verbose_name_plural = _('Text Phrases')


class TextImagePhraseAbstractModel(PublicFields):
    position = models.CharField(max_length=255, verbose_name=_('Location'))

    def __str__(self):
        return self.title

    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        abstract = True
        verbose_name = _('Text & Image Phrase')
        verbose_name_plural = _('Text & Image Phrases')
