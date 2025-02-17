from django import forms


class PlaceForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    isOpen = forms.BooleanField(initial=True, required=False)
    image = forms.CharField(max_length=500, required=False)
