from django import forms
from .models import Books


class bookform(forms.ModelForm):
    class Meta:
        model=Books
        fields=['name','desc','year','img','pdf']