from django import forms


class AnimalForm(forms.Form):
    name = forms.CharField(max_length=100)

    scientificName = forms.CharField()

    habitat = forms.CharField(required=False)

    diet = forms.CharField(required=False)

    behaviour = forms.CharField(required=False)

    weightMale = forms.CharField(required=False)
    weightMale = forms.CharField(required=False)

    image = forms.CharField(max_length=500, required=False)

    conservationStatus = forms.CharField(required=False)

    funFacts = forms.CharField(max_length=500)
