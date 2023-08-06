from django.forms import ModelForm

from .models import *

__all__ = (
    'ScriptBlockForm',
)


class ScriptBlockForm(ModelForm):
    
    class Meta:
        model = ScriptBlock
        fields = '__all__'

    def clean(self):
        allowed = self.cleaned_data['allowed']
        disallowed = self.cleaned_data['disallowed']

        if not (allowed or disallowed):
            script_url, created = ScriptUrl.objects.get_or_create(
                pattern='/*'
            )
            self.cleaned_data['allowed'] = (script_url, )
        return self.cleaned_data