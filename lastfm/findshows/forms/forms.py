from django import forms

class ShowsForm(forms.Form):
    username = forms.CharField(max_length=100)
