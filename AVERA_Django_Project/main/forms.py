from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Gift, Feedback, Wishlist

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=80, required=True)
    last_name = forms.CharField(max_length=80, required=False)
    phone = forms.CharField(max_length=30, required=False)
    address = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ("username","first_name","last_name","email","phone","address","password1","password2")

class GiftForm(forms.ModelForm):
    class Meta:
        model = Gift
        fields = ("gift_type","description","quantity","organization")
        widgets = {"description": forms.Textarea(attrs={"rows":4})}

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ("message","photo")
        widgets = {"message": forms.Textarea(attrs={"rows":5})}

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ("organization","title","description","item_name","quantity_needed","priority")
        widgets = {"description": forms.Textarea(attrs={"rows":4})}
