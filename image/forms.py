from django import forms


class UploadForm(forms.Form):
    file = forms.ImageField(label='画像ファイル')
