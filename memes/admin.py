from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from .models import Meme


class MemeAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'thumbnail', 'pub_date', 'post_url', 'views', 'valid',)
    list_editable = ('valid', 'views')
    fields = ('views', 'thumbnail',)
    ordering = ('-pub_date',)

    def thumbnail(self, obj):
        return format_html(u'<img src="%s" height="400" width="400"/>' % obj.image_url)

    thumbnail.allow_tags = True


admin.site.register(Meme, MemeAdmin)
