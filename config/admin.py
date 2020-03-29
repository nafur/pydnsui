from django.contrib import admin
from config.models import *

class RecordAdmin(admin.ModelAdmin):
    readonly_fields=('zone',)

admin.site.register(Zone)
admin.site.register(Record)
