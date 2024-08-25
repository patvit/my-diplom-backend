from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import CustomUser
from storage.models import Document


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    max_num = 0
    exclude = ('file_url', 'file',)
    readonly_fields = ('upload_datetime', 'share_link')


class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    inlines = (DocumentInline,)
    list_filter = ()
    list_display = ('username', 'joined_at', 'document_count',
                    'is_active', 'is_staff',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    def document_count(self, obj):
        return obj.document_set.count()


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.unregister(Group)