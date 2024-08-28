from django import forms


class AddPlaceForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    isOpen = forms.BooleanField(initial=True)

    animal_id = forms.IntegerField(required=False)
    image = forms.CharField(max_length=500, required=False)
