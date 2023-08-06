# Django Tools SocialNetworks

Simple Django app to manage a website social network links

## Installation

1. Install with pip install `django-tools-socialnetworks`.

2. Add `djtools.socialnetworks` to your INSTALLED_APPS setting like this:
```
INSTALLED_APPS = [
    ...
    'djtools.socialnetworks',
]
```

3.1 Add the context processor to your settings file if need the social networks in all your pages.
```
TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                'djtools.socialnetworks.context_processors.social_networks',
            ],
        },
    },
]
```
3.2 Or extend the `get_context` function of your view like this:
```
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['social_networks'] = SocialNetwork.get_social_networks()
    return context
```

4. Run migrations commands `python manage.py migrate`

5. Include social_networks.html snippet in your template or override it.
```
{% include "djtools/socialnetworks/social_networks.html" %}
```
