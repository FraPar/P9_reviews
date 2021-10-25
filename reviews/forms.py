from django import forms

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


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class FollowedUserForm(forms.ModelForm):
    
    class Meta:
        model = models.Review
        fields = ['user']


class DeleteFollowedUserForm(forms.Form):
    delete_follow = forms.BooleanField(widget=forms.HiddenInput, initial=True)