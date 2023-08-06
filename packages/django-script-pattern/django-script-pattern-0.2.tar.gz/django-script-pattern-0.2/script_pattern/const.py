from django.utils.translation import pgettext_lazy

__all__ = (
    'TAGS',
    'TAGS_ID_MAP',
    
    'POSITIONS',
    'POSITIONS_ID_MAP'
)

TAG_HEAD = 'head'
TAG_BODY = 'body'
TAGS = (
    (TAG_HEAD, pgettext_lazy("script_pattern", "Head")),
    (TAG_BODY, pgettext_lazy("script_pattern", "Body"))
)

POS_TOP ='top'
POS_BOTTOM = 'bottom'
POSITIONS = (
    (POS_TOP, pgettext_lazy("script_pattern", "Top")),
    (POS_BOTTOM, pgettext_lazy("script_pattern", "Bottom"))
)