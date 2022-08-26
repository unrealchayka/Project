from django import forms

from Shop.models import *


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)


class CheckoutForm(forms.ModelForm):

    class Meta:
        model = Checkout
        fields = ('product', 'addreses', 'town', 'comment', 'payment')


class CastomUserForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name','email', 'social_network', 'photo')


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('text',)


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('quantit', )

