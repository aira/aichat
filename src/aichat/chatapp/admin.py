from django.contrib import admin

from .models import TriggerResponse, Node, Edge


class TriggerResponseAdmin(admin.ModelAdmin):
    list_display = ('source_state', 'dest_state', 'trigger', 'response')


class NodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'x_loc', 'y_loc')


class EdgeAdmin(admin.ModelAdmin):
    list_display = ('trigger', 'response')


class TriggerResponseAdminFK(admin.ModelAdmin):
    list_display = ('source_state', 'dest_state', 'trigger', 'response')


admin.site.register(TriggerResponse, TriggerResponseAdmin)
admin.site.register(Edge, EdgeAdmin)
admin.site.register(Node, NodeAdmin)
