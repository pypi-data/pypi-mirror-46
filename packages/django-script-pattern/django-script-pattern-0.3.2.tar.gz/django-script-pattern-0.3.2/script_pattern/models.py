from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import pgettext_lazy

from script_pattern import const

__all__ = (
    'ScriptUrl',
    'ScriptBlock'
)


class ScriptUrl(models.Model):
    pattern = models.CharField(
        pgettext_lazy("script_pattern", "Pattern"), max_length=450,
        help_text=pgettext_lazy(
            "script_pattern", 
            "Case-sensitive. A missing trailing slash does "
            "also match to files which start with the name of "
            "the pattern, e.g., '/admin' matches '/admin.html' too. "
            "Also pattern allow an asterisk (*) as a wildcard "
            "and a dollar sign ($) to "
            "match the end of the URL, e.g., '/*.jpg$'."
        )
    )

    class Meta:
        verbose_name = pgettext_lazy(
            "script_pattern", "Script url"
        )
        verbose_name_plural = pgettext_lazy(
            "script_pattern", "Script urls"
        )

    def __str__(self):
        return self.pattern

    def save(self, *args, **kwargs):
        if not self.pattern.startswith('/'):
            self.pattern = '/' + self.pattern
        super().save(*args, **kwargs)


class ScriptBlock(models.Model):
    name = models.CharField(
        pgettext_lazy("script_pattern", "Name"), max_length=450
    )
    is_active = models.BooleanField(
        pgettext_lazy("script_pattern", "Is active"), default=True
    )
    tag = models.CharField(
        pgettext_lazy("script_pattern", "Tag"), max_length=50,
        choices=const.TAGS,
        default=const.TAG_HEAD
    )
    position = models.CharField(
        pgettext_lazy("script_pattern", "Position"), max_length=50,
        choices=const.POSITIONS,
        default=const.POS_TOP
    )
    script = models.TextField(
        pgettext_lazy("script_pattern", "Script")
    )
    allowed = models.ManyToManyField(
        ScriptUrl, blank=True,
        related_name="allowed",
        verbose_name=pgettext_lazy("script_pattern", "Allowed"),
        help_text=pgettext_lazy(
            "script_pattern",
            "The URLs which are allowed to include script block."
        )
    )
    disallowed = models.ManyToManyField(
        ScriptUrl, blank=True, 
        related_name="disallowed",
        verbose_name=pgettext_lazy("script_pattern", "Disallowed"),
        help_text=pgettext_lazy(
            "script_pattern",
            "The URLs which are not allowed to include script block."
        )
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = pgettext_lazy(
            "script_pattern", "Script block"
        )
        verbose_name_plural = pgettext_lazy(
            "script_pattern", "Script blocks"
        )
        ordering = ('order', )

    def __str__(self):
        return self.name
