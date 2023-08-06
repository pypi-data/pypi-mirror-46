from django import forms
from django.conf import settings

def get_action_url(**kwargs):
    action_url = getattr(settings, 'SPGATEWAY_MPG_ACTION', default=None)
    if not action_url:
        merchant_id = kwargs.get('MerchantID', settings.SPGATEWAY_MERCHANTID)
        merchant_profile = settings.SPGATEWAY_PROFILE[merchant_id]
        action_url = merchant_profile.get('MPG_ACTION')
    if not action_url:
        debug = merchant_profile.get('DEBUG', getattr(settings, 'DEBUG', default=None))
        if debug:
            action_url = 'https://ccore.spgateway.com/MPG/mpg_gateway'
        else:
            action_url = 'https://core.spgateway.com/MPG/mpg_gateway'
    return action_url


class SpgatewayForm(forms.Form):
    MerchantID = forms.CharField(max_length=15, widget=forms.HiddenInput())
    TradeInfo = forms.CharField(widget=forms.HiddenInput())
    TradeSha = forms.CharField(widget=forms.HiddenInput())
    Version = forms.CharField(max_length=5, initial='1.4', widget=forms.HiddenInput())
    action = get_action_url()
