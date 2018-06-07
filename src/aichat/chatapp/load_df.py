from __future__ import print_function
import os
import json
import pandas as pd
import dialog_graph
import regex
from aichat import pattern
from aichat.constants import DATA_DIR


def load_df(path=DATA_DIR):
    """
    >>> df = load_df()
    >>> df.head(1)  # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
                                                   trigger ...
    >>> len(load_df()) > 200
    True
        """
    CSV_COLUMNS = ('trigger', 'response', 'source_state', 'dest_state')
    df = pd.DataFrame(columns=CSV_COLUMNS)
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".csv"):
                dfadd = pd.read_csv(path + '/' + file)
                dfadd.columns = CSV_COLUMNS[:len(dfadd.columns)]
                df = df.append(dfadd)

    df_clean = pd.DataFrame(columns=CSV_COLUMNS, index=None)
    for column in CSV_COLUMNS:
        df_clean[column] = df[column]
    df_clean.to_csv("Export.csv", index=None)
    df_clean = df_clean.reset_index(drop=True)
    df_clean = df_clean.fillna('root')
    return df_clean


DF = load_df()


def nodes_to_list(path=DATA_DIR):
    """ returns list of all fixed non pattern nodes names

    >>> sorted([sorted(list(d.items())) for d in nodes_to_list()])
    [[('id', 'node0'), ('name', 'Bluetooth connecting headset')],
     [('id', 'node1'), ('name', 'Bluetooth connecting paired')],
     [('id', 'node10'), ('name', 'Chloe Skill Quickstart')],
     [('id', 'node11'), ('name', 'Chloe Skill Time Date')],
     [('id', 'node12'), ('name', 'Tutorial Done')],
     [('id', 'node13'), ('name', 'Tutorial Last Tip')],
     [('id', 'node14'), ('name', 'Tutorial Setup')],
     [('id', 'node15'), ('name', 'Tutorial Start')],
     [('id', 'node16'), ('name', 'riddle 1 1')],
     [('id', 'node17'), ('name', 'riddle 1 2')],
     [('id', 'node18'), ('name', 'riddle 2 1')],
     [('id', 'node19'), ('name', 'riddle 3 1')],
     [('id', 'node2'), ('name', 'Bluetooth connecting speaker')],
     [('id', 'node20'), ('name', 'root')],
     [('id', 'node3'), ('name', 'Bluetooth disconnect')],
     [('id', 'node4'), ('name', 'Call Agent')],
     [('id', 'node5'), ('name', 'Chloe Skill Call Agent')],
     [('id', 'node6'), ('name', 'Chloe Skill Flashlight')],
     [('id', 'node7'), ('name', 'Chloe Skill Jokes')],
     [('id', 'node8'), ('name', 'Chloe Skill Jokes Repeat')],
     [('id', 'node9'), ('name', 'Chloe Skill Privacy Mode')]]


    """
    node_list = sorted(set(list(set(DF.dest_state.fillna('root'))) + list(set(DF.source_state.fillna('root')))))
    dict_list = []
    node_index = 0
    for node in node_list:
        if '*' in node or '?' in node:
            continue
        dict_list.append(
            {'name': node, 'id': 'node' + str(node_index)})
        node_index = node_index + 1
    return dict_list


def links_to_list(path=DATA_DIR, value=1):

    links = []
    node_names = list(set(DF.dest_state))
    for i, source_pattern in enumerate(DF.source_state.values):
        patt = pattern.expand_globstar(source_pattern)
        for j, name in enumerate(node_names):
            if ('{' in patt or '[' in patt) and regex.match(patt, name):
                print(str(j) + source_pattern + ',' + name)
                if ('*' in name or '?' in name):
                    pass
                else:
                    links.append({'source': node_names.index(name),
                                  'target': node_names.index(DF.dest_state.values[i]),
                                  'command': DF.trigger[i],
                                  'response': DF.response[i],
                                  'value': value})
            elif source_pattern == name:
                if ('*' in name or '?' in name):
                    pass
                else:
                    print("nonpattern:" + str(j) + source_pattern + ',' + name)
                    links.append({'source': node_names.index(name),
                                  'target': node_names.index(DF.dest_state.values[i]),
                                  'command': DF.trigger[i],
                                  'response': DF.response[i],
                                  'value': value})
    return links


def node_filter(pattern, names=nodes_to_list()):
    return [name for name in names if regex.match(pattern, name)]


def is_globstar(node_name):
    return True if '*' in node_name or '?' in node_name or '|' in node_name else False


def links_to_list2(path=DATA_DIR, value=1):
    links = []
    nonpattern_node_names = nodes_to_list()
    node_names = list(set(DF.dest_state))
    for i, source_pattern in enumerate(DF.source_state.values):
        source_patt = pattern.expand_globstar(source_pattern)
        for j, dest_pattern in enumerate(node_names):
            dest_patt = pattern.expand_globstar(dest_pattern)
            if ('{' in source_patt or '[' in source_patt) and regex.match(source_patt, source_pattern):
                print(str(j) + source_pattern + ',' + dest_pattern)
                if ('{' in dest_patt or '[' in dest_patt) and regex.match(dest_patt, dest_pattern):
                    print(str(j) + dest_patt + ',' + dest_pattern)
                    for dest_node in nonpattern_node_names:
                        links.append({'source': nonpattern_node_names.index(source_pattern),
                                      'target': nonpattern_node_names.index(DF.dest_node.values[i]),
                                      'command': DF.trigger[i],
                                      'response': DF.response[i],
                                      'value': value})
                else:
                    links.append({'source': nonpattern_node_names.index(source_pattern),
                                  'target': nonpattern_node_names.index(DF.dest_state.values[j]),
                                  'command': DF.trigger[i],
                                  'response': DF.response[i],
                                  'value': value})
            elif source_pattern == dest_pattern:
                if ('*' in dest_pattern or '?' in dest_pattern):
                    pass
                else:
                    print("nonpattern:" + str(j) + source_pattern + ',' + dest_pattern)
                    links.append({'source': nonpattern_node_names.index(dest_pattern),
                                  'target': nonpattern_node_names.index(dest_pattern),
                                  'command': DF.trigger[i],
                                  'response': DF.response[i],
                                  'value': value})
    return links


def gen_links(path=DATA_DIR, value=1, df=DF):
    """ returns a d3 graph datastructure

    >>> df = pd.DataFrame([['', '', 1, 2]], columns=('trigger', 'response', 'source_state', 'dest_state'))
    >>> gen_links(path=DATA_DIR, value=1, df=df)
    {
      "directed": true,
      "multigraph": false,
      "name": "Dialog",
      "nodes": [
        {
          "name": "1",
          "id": "node0"
        },
        {
          "name": "2",
          "id": "node1"
        }
      ],
      "links": [
        {
          "source": 0,
          "target": 1,
          "command": "",
          "response": "",
          "value": 1
        }
      ]
    }
    """
    links = []
    node_names = nodes_to_list()
    for source_index, source_name in enumerate(df.source_state.values):
        if not is_globstar(source_name):
            current_dest_name = df.dest_state[source_index]
            if not is_globstar(current_dest_name):
                links.append({'source': node_names.index(source_name),
                              'target': node_names.index(current_dest_name),
                              'command': df.trigger[source_index],
                              'response': df.response[source_index],
                              'value': value})


def create_json(path=DATA_DIR):
    dialog = dialog_graph.base_dialog()
    dialog['nodes'] = nodes_to_list()
    dialog['links'] = links_to_list()
    js = json.dumps(dialog, indent=2)
    with open("../data/newdialog.json", "w") as f:
        f.write(js)
    return js


if __name__ == "__main__":
    df = load_df()
