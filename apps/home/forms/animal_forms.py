from django import forms


class AddAnimalForm(forms.Form):
    name = forms.CharField(max_length=100)
    image = forms.CharField(max_length=500, required=False)
