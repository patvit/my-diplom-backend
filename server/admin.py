from django.contrib import admin

# Register your models here.

from django.utils.html import format_html

from . import models


@admin.register(models.Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('filename', 'upload_datetime', 'uploaded_by', 'download_link', 'share_link')
    readonly_fields = ('share_link', 'size',)

    def download_link(self, obj):
        return format_html(
            "<a href='%s' target='_blank'><button type='button'>Download</button></a>" % (obj.share_link,))

    download_link.short_description = 'Download Link'