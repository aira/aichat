from django.db import models
from django.db.models import CharField, TextField, NullBooleanField, DateTimeField, IntegerField
from aichat import pattern
import regex
CHOICES_IS_GLOBSTAR = ((None, ''), (True, 'Yes'), (False, 'No'))


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
        for obj in TriggerResponse.objects.all():
            nodes.append(obj.dest_state)
        nodes = list(set(nodes))

        node_index = 0
        for node in nodes:
            js["nodes"].append({'name': node, 'id': 'node' + str(node_index)})
            node_index = node_index + 1

        for i, obj in enumerate(TriggerResponse.objects.all()):
            source_pattern = obj.source_state
            patt = pattern.expand_globstar(source_pattern)
            for j, name in enumerate(nodes):
                if ('{' in patt or '[' in patt) and regex.match(patt, name):
                    print(str(j) + source_pattern + ',' + name)
                    links.append({'source': nodes.index(name),
                                  'target': nodes.index(obj.dest_state),
                                  'command': obj.trigger,
                                  'response': obj.response,
                                  'value': value})
                elif source_pattern == name:
                    print("nonpattern:" + str(j) + source_pattern + ',' + name)
                    links.append({'source': nodes.index(name),
                                  'target': nodes.index(obj.dest_state),
                                  'command': obj.trigger,
                                  'response': obj.response,
                                  'value': value})

        js["links"] = links
        # js = json.dumps(js, indent=2)
        # use nodes and edges to populate a json string like load.py
    return js
