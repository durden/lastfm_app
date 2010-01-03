"""Form classes for lastfm show searches"""

from django import forms


class ShowsForm(forms.Form):
    """Form to collect lastfm username and city/state for upcoming shows"""

    username = forms.CharField(max_length=100)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=2)
