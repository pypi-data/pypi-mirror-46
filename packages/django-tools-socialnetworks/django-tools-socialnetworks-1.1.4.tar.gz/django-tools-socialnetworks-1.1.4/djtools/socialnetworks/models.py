from django.db import models


class AbstractSocialNetwork(models.Model):
    SOCIAL_NETWORKS = {
        'facebook': {
            'name': 'Facebook',
            'link': 'https://www.facebook.com/',
            'icon': 'facebook',
        },
        'instagram': {
            'name': 'Instagram',
            'link': 'https://www.instagram.com/',
            'icon': 'instagram',
        },
        'twitter': {
            'name': 'Twitter',
            'link': 'https://twitter.com/',
            'icon': 'twitter',
        },
        'youtube': {
            'name': 'YouTube',
            'link': 'https://www.youtube.com/channel/',
            'icon': 'youtube',
        },
        'vimeo': {
            'name': 'Vimeo',
            'link': 'https://vimeo.com/',
            'icon': 'vimeo',
        },
        'github': {
            'name': 'GitHub',
            'link': 'https://github.com/',
            'icon': 'github',
        },
        'behance': {
            'name': 'Behance',
            'link': 'https://www.behance.net/',
            'icon': 'behance',
        },
        'pinterest': {
            'name': 'Pinterest',
            'link': 'https://pinterest.com/',
            'icon': 'pinterest',
        },
    }

    social_network = models.CharField(max_length=255)
    account_id = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ('order',)

    def __str__(self):
        return self.get_name()

    @classmethod
    def get_choices(cls):
        return [
            (social_network_id, social_network_info['name'])
            for social_network_id, social_network_info in cls.SOCIAL_NETWORKS.items()
        ]

    @classmethod
    def get_social_networks(cls):
        return cls.objects.all()

    @property
    def info(self):
        return self.SOCIAL_NETWORKS.get(self.social_network, {})

    def get_name(self):
        return self.info.get('name')

    def get_link(self):
        return f"{self.info.get('link')}{self.account_id}"

    def get_icon(self):
        return self.info.get('icon')


class SocialNetwork(AbstractSocialNetwork):
    pass
