from django.contrib import admin
from .models import KeyWord, Documents, Authors

# Register your models here.


class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('title', 'abstract', 'document')

admin.site.register(Documents, DocumentsAdmin)
admin.site.register(KeyWord)
admin.site.register(Authors)
