from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


class ScriptPatternConfig(AppConfig):
    name = 'script_pattern'
    verbose_name = pgettext_lazy("script_pattern", "Script pattern")
