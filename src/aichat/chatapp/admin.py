from django.contrib import admin

from .models import TriggerResponse, node, edge


class TriggerResponseAdmin(admin.ModelAdmin):
    list_display = ('source_state', 'dest_state', 'trigger', 'response')


class edgeAdmin(admin.ModelAdmin):
    list_display = ('trigger', 'response')


admin.site.register(TriggerResponse, TriggerResponseAdmin)
admin.site.register(edge, edgeAdmin)
admin.site.register(node)
