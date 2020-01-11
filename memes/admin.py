from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from .models import Meme


class MemeAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'pub_date', 'views', 'valid',)
    list_editable = ('valid',)

    fields = ('views', 'thumbnail',)

    def thumbnail(self, obj):
        return format_html(u'<img src="%s" height="300" width="300"/>' % obj.image_url)

    thumbnail.allow_tags = True


admin.site.register(Meme, MemeAdmin)
