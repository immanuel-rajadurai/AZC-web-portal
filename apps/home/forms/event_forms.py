from django import forms


class CreateEventForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)

    place_id = forms.CharField(required=False, widget=forms.RadioSelect)

    image = forms.CharField(max_length=500)
