from django import forms

from . import models


""" class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['image'] """

class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
