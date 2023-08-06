from django.contrib import admin
from django.utils.translation import pgettext_lazy

from adminsortable2.admin import SortableAdminMixin

from .models import *
from .forms import ScriptBlockForm


__all__ = (
    'ScriptBlockAdmin',
)


admin.site.register(ScriptUrl)


@admin.register(ScriptBlock)
class ScriptBlockAdmin(
    SortableAdminMixin,
    admin.ModelAdmin
):
    form = ScriptBlockForm
    list_display = (
        'name',
        'tag',
        'position',
        'is_active'
    )
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'is_active'),
                ('tag', 'position'),
                'script'
            )
        }),
        (pgettext_lazy("script_pattern", "Url patterns"), {
            'fields': (
                'allowed',
                'disallowed'
            )
        })
    )
