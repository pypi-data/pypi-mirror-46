from django import forms

from .models import SocialNetwork


class SocialNetworkForm(forms.ModelForm):
    social_network = forms.ChoiceField(choices=SocialNetwork.get_choices)

    class Meta:
        model = SocialNetwork
        fields = ('social_network', 'account_id', 'order')
