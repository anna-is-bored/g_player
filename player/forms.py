from django import forms

from .models import Track
from .utils import Utils
from .validation import PlayerValidator


class TrackSearchForm(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Name',
                                                                   'class': 'form-control'}))

    class Meta:
        model = Track
        fields = ['name']


class TrackCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TrackCreateForm, self).__init__(*args, **kwargs)
        # add nice styling to the form
        Utils.add_form_control_class(self)

        # basic validation, more validation could be added, for example prevent duplication
        self.fields['name'].validators.append(PlayerValidator.validate_track_name)

    class Meta:
        model = Track
        fields = ['name', 'duration', 'artist']


