from django import forms
from django.core.exceptions import ValidationError

class SqLikeForm:
    def __init__(self, *args, sqlike=None, **kwargs):
        self.sqlike = sqlike
        super(SqLikeForm, self).__init__(*args, **kwargs)

    def clean(self):
        super(SqLikeForm, self).clean()
        pattern = self.cleaned_data.get('pattern')

        try:
            self.sqlike.feed(pattern)
        except KeyError as exc:
            raise forms.ValidationError("Invalid attribute: %s " % exc)
        except ValidationError as exc:
            raise forms.ValidationError(exc)


