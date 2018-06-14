from django.db import models
from django.db.models import CharField, TextField, NullBooleanField, DateTimeField, IntegerField
from aichat import pattern
import regex
from dal import autocomplete

CHOICES_IS_GLOBSTAR = ((None, ''), (True, 'Yes'), (False, 'No'))


def get_nodes():
    nodes = []
    for object in TriggerResponse.objects.all():
        nodes.append(object.source_state)
        nodes.append(object.dest_state)
    nodes = sorted(set(list(set(nodes))))
    return [node for node in nodes if '*' not in node and '?' not in node and '|' not in node]


def is_globstar(node_name):
    if '*' in node_name or '?' in node_name or '|' in node_name:
        return True
    else:
        False


class TimestampedModel(models.Model):
    """ Abstract base class with self-updating ``created`` and ``modified`` fields. """
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AuthoredModel(TimestampedModel):
    """ Abstract base class with ``author`` field. """
    author = CharField(max_length=100)

    class Meta:
        abstract = True


class TriggerResponse(AuthoredModel):
    trigger = CharField(max_length=200)
    response = TextField()
    source_state = CharField(max_length=200)
    dest_state = CharField(max_length=200)
    is_globstar = NullBooleanField(choices=CHOICES_IS_GLOBSTAR, max_length=3, null=True, blank=True, default=None)

    def __str__(self):
        return self.source_state + ' to ' + self.dest_state


class node(models.Model):
    name = CharField(max_length=200, default='')
    x_loc = IntegerField(default=0)
    y_loc = IntegerField(default=0)

    def __str__(self):
        return self.name


class edge(models.Model):
    trigger = CharField(max_length=200, default='')
    response = CharField(max_length=200, default='')
    source = models.ForeignKey(node, on_delete=models.CASCADE, related_name='source', null=True)
    dest = models.ForeignKey(node, on_delete=models.CASCADE, related_name='dest', null=True)
    is_globstar = NullBooleanField(choices=CHOICES_IS_GLOBSTAR, max_length=3, null=True, blank=True, default=None)

    def __str__(self):
        return self.trigger + ' to ' + self.response


# class node_autocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         objects = TriggerResponse.objects.all()
#         if self.q:
#             objects = objects.filter(source_state__istartswith=self.q)
#         return objects
class node_autocomplete(autocomplete.Select2ListView):
    def get_list(self):
        nodes = get_nodes()
        nodes = [node for node in nodes if node.startswith(self.q)]
        return nodes


def get_network(qs=None, value=1):
    if qs is None:
        # query database for nodes and edges
        js = {
            "directed": True,
            "multigraph": False,
            "name": "Dialog",
            "nodes": [],
            "links": []
        }
        nodes = []
        links = []
        node_names = get_nodes()

        node_index = 0
        for node in node_names:
            if '*' in node or '?' in node or '|' in node:
                continue
            nodes.append(
                {'name': node, 'id': 'node' + str(node_index)})
            node_index = node_index + 1

        for source_obj in TriggerResponse.objects.all():
            if not is_globstar(str(source_obj.source_state)):
                current_dest_name = source_obj.dest_state
                if not is_globstar(str(current_dest_name)):
                    links.append({'source': node_names.index(source_obj.source_state),
                                  'target': node_names.index(current_dest_name),
                                  'command': source_obj.trigger,
                                  'response': source_obj.response,
                                  'value': value})
                else:
                    dest_pattern = pattern.expand_globstar(current_dest_name)
                    for dest_node in node_names:
                        if regex.match(dest_pattern, dest_node):
                            links.append({'source': node_names.index(source_obj.source_state),
                                          'target': node_names.index(current_dest_name),
                                          'command': source_obj.trigger,
                                          'response': source_obj.response,
                                          'value': value})
            else:
                if not is_globstar(source_obj.dest_state):
                    current_dest_name = source_obj.dest_state
                    current_trig = source_obj.trigger
                    current_resp = source_obj.response
                    source_pattern = pattern.expand_globstar(source_obj.source_state)
                    for source_obj_index, source_obj in enumerate(TriggerResponse.objects.all()):
                        if regex.match(source_pattern, source_obj.source_state) and not is_globstar(source_obj.source_state):
                            links.append({'source': node_names.index(source_obj.source_state),
                                          'target': node_names.index(current_dest_name),
                                          'command': current_trig,
                                          'response': current_resp,
                                          'value': value})
                else:
                    source_pattern = pattern.expand_globstar(source_obj.source_state)
                    current_dest_name = source_obj.dest_state
                    dest_pattern = pattern.expand_globstar(current_dest_name)
                    for current_source_index, current_source_name in enumerate(node_names):
                        if regex.match(source_pattern, current_source_name) and not is_globstar(current_source_name):
                            for dest_index, dest_name in enumerate(node_names):
                                if regex.match(dest_pattern, dest_name) and not is_globstar(dest_name):
                                    links.append({'source': node_names.index(current_source_name),
                                                  'target': node_names.index(dest_name),
                                                  'command': source_obj.trigger,
                                                  'response': source_obj.response,
                                                  'value': value})
    js["nodes"] = nodes
    js["links"] = links
    return js
