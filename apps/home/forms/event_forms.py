from django import forms


class CreateEventForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    place_id = forms.IntegerField()
    image = forms.CharField(max_length=500)

    animal_id = forms.IntegerField(required=False)
