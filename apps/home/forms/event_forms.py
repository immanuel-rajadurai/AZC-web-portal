from django import forms


class EventForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    image = forms.CharField(max_length=500, required=False)

    tags = forms.CharField(max_length=500, required=False)
