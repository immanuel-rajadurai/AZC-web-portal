from django import forms


class PlaceForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    isOpen = forms.BooleanField(initial=True, required=False)
    image = forms.CharField(max_length=500, required=False)
