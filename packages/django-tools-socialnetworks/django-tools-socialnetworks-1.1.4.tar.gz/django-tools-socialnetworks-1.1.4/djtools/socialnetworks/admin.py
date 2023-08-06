from django.contrib import admin
from django.utils.safestring import mark_safe

from .forms import SocialNetworkForm
from .models import SocialNetwork


@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'order',
        'link',
    ]
    form = SocialNetworkForm

    def link(self, obj):
        link = obj.get_link()
        return mark_safe('<a href="%s" target="_blank">%s</a>' % (link, link))
