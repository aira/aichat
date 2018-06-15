from django.contrib import admin

from .models import TriggerResponse, Node, Edge, TriggerResponseFK


class TriggerResponseAdmin(admin.ModelAdmin):
    list_display = ('source_state', 'dest_state', 'trigger', 'response')


class edgeAdmin(admin.ModelAdmin):
    list_display = ('trigger', 'response')


admin.site.register(TriggerResponse, TriggerResponseAdmin)
admin.site.register(Edge, edgeAdmin)
admin.site.register(Node)
admin.site.register(TriggerResponseFK)
