from django import forms
from django.forms.widgets import TextInput

from . import models

""" class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['image'] """


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class' : "form-control"}),
            'description': forms.TextInput(attrs={'class' : "form-control"}),
        }


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']
        widgets = {
            'headline': forms.TextInput(attrs={'class' : "form-control"}),
            'rating': forms.RadioSelect(
                choices=[
                    (0, '0'),
                    (1, '1'),
                    (2, '2'),
                    (3, '3'),
                    (4, '4'),
                    (5, '5'),
                ],
                attrs={"required": True}
                ),
            'body': forms.TextInput(attrs={'class' : "form-control"}),
        }


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class DeleteFollowedUserForm(forms.Form):
    delete_follow = forms.BooleanField(widget=forms.HiddenInput, initial=True)