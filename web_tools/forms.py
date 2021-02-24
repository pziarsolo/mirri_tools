from django import forms


class ValidationUploadForm(forms.Form):
    file = forms.FileField(
        max_length=100, label="Add an excel file with the MIRRI specs", required=True
    )
    do_upload = forms.BooleanField(
        label='Check it if you want to uploaad the file', required=False)
