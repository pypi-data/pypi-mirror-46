from django import forms


class CoverPageViewForm(forms.Form):
    redirect = forms.CharField(required=False)
