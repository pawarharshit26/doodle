from django import forms

class ImageuploadForm(forms.Form):
   image = forms.ImageField() 