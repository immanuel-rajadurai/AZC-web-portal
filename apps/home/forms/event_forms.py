from django import forms


class CreateEventForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)

    # TODO: change appropriately as foreign key link
    place_id = forms.IntegerField(required=False)

    image = forms.CharField(max_length=500)
