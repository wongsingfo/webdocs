from django.contrib import admin

# Register your models here.

from .models import Document


class DocumentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,      {'fields': ['title']}),
        ('Details', {'fields': ['body', 'last_modified']}),
    ]
    list_display = ('title', 'last_modified')
    list_filter = ['last_modified']


admin.site.register(Document, DocumentAdmin)
