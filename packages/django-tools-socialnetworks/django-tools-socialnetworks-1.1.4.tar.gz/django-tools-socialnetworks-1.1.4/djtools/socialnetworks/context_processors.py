from .models import SocialNetwork


def social_networks(request):
    return {
        'social_networks': SocialNetwork.get_social_networks()
    }
