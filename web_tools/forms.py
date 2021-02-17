from django import forms


class ValidationUploadForm(forms.Form):
    file = forms.FileField(
        max_length=100, label="Add an escel file with the MIRRI specs", required=True
    )
