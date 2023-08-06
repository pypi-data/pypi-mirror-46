import re

from django import template
from django.utils.safestring import mark_safe

from django_jinja import library

from script_pattern.const import (
    TAGS,
    POSITIONS
)
from script_pattern.models import ScriptBlock

__all__ = (
    'get_script_pattern',
)

register = template.Library()


def is_allowed(path, block):
    for url in block.allowed.all():
        pattern = url.pattern.replace('*', '(.*)')
        is_match = bool(re.search(pattern, path))
        if is_match:
            return True


def is_disallowed(path, block):
    for url in block.disallowed.all():
        pattern = url.pattern.replace('*', '(.*)')
        is_match = bool(re.search(pattern, path))
        if is_match:
            return True


@library.global_function
@register.simple_tag
def get_script_pattern(request, tag, position):
    if not (
        tag in dict(TAGS).keys()
        and position in dict(POSITIONS).keys()
    ):
        return ''

    path = request.get_full_path()
    blocks = ScriptBlock.objects.filter(
        is_active=True,
        tag=tag,
        position=position
    ).prefetch_related(
        'allowed',
        'disallowed'
    )
    for block in blocks:
        if (
            not is_disallowed(path, block)
            and is_allowed(path, block)
        ):
            return mark_safe(block.script)
    return ''
