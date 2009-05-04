from django import forms

class ShowsForm(forms.Form):
    username = forms.CharField(max_length=100)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=2)
