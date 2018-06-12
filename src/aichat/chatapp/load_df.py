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
    if os.path.isfile(path):
        dfadd = pd.read_csv(path)
        dfadd.columns = CSV_COLUMNS[:len(dfadd.columns)]
        df = df.append(dfadd)
    else:
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

# gen_nodes returns list of nodes for the value of the base d3 'nodes': json


def gen_nodes(path=DATA_DIR, DF=DF):
    """ returns list of all fixed non pattern nodes names

    >>> sorted([sorted(list(d.items())) for d in gen_nodes()])
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

# is glob_star returns true if node is a golbstar


def is_globstar(node_name):
    if '*' in node_name or '?' in node_name or '|' in node_name:
        return True
    else:
        False


def get_nodes(path=DATA_DIR, DF=DF):
    node_list = sorted(set(list(set(DF.dest_state.fillna('root'))) + list(set(DF.source_state.fillna('root')))))
    return [node for node in node_list if '*' not in node and '?' not in node and '|' not in node]


def node_filter(pattern, names=get_nodes()):
    return [name for name in names if regex.match(pattern, name)]

# gen_nodes returns list of links for the value of the base d3 'links': json


def gen_links(path=DATA_DIR, value=1, df=DF):
    """ returns links for the d3 structure

    # Case1 nopatt
    >>> df = pd.DataFrame([['1 goto 2', 'okay', '1', '2']], columns=('trigger', 'response', 'source_state', 'dest_state'))
    >>> gen_links(path=DATA_DIR, value=1, df=df)
    [{'source': 0, 'target': 1, 'command': '1 goto 2', 'response': 'okay', 'value': 1}]

    # Case3 destpatt
    >>> df = pd.DataFrame([['1 goto 2', 'okay', '1', '2'], ['2 goto 3', 'okay', '2', '3'], ['3 goto 4', 'okay', '3', '4'], ['4 goto 1 or 2', 'okay', '4', '1|2']], columns=('trigger', 'response', 'source_state', 'dest_state')) # noqa
    >>> gen_links(path=DATA_DIR, value=1, df=df)
    [{'source': 0, 'target': 1, 'command': '1 goto 2', 'response': 'okay', 'value': 1},
     {'source': 1, 'target': 2, 'command': '2 goto 3', 'response': 'okay', 'value': 1},
     {'source': 2, 'target': 3, 'command': '3 goto 4', 'response': 'okay', 'value': 1},
     {'source': 3, 'target': 1, 'command': '4 goto 1 or 2', 'response': 'okay', 'value': 1}]

    # Case2 sourcepatt
    >>> df = pd.DataFrame([['', '', '1', '2'], ['', '', '2', '3'], ['', '', '3', '4'], ['', '', '1|2', '5']], columns=('trigger', 'response', 'source_state', 'dest_state')) # noqa
    >>> gen_links(path=DATA_DIR, value=1, df=df)
    [{'source': 0, 'target': 1, 'command': '', 'response': '', 'value': 1},
     {'source': 1, 'target': 2, 'command': '', 'response': '', 'value': 1},
     {'source': 2, 'target': 3, 'command': '', 'response': '', 'value': 1},
     {'source': 0, 'target': 4, 'command': '', 'response': '', 'value': 1},
     {'source': 1, 'target': 4, 'command': '', 'response': '', 'value': 1}]

    # Case4 sourcepatt and destpatt
    >>> df = pd.DataFrame([['', '', '1', '2'], ['', '', '2', '3'], ['', '', '3', '4'], ['', '', '2|3', '1|2']], columns=('trigger', 'response', 'source_state', 'dest_state')) # noqa
    >>> gen_links(path=DATA_DIR, value=1, df=df)
    [{'source': 0, 'target': 1, 'command': '', 'response': '', 'value': 1},
     {'source': 1, 'target': 2, 'command': '', 'response': '', 'value': 1},
     {'source': 2, 'target': 3, 'command': '', 'response': '', 'value': 1},
     {'source': 1, 'target': 1, 'command': '', 'response': '', 'value': 1},
     {'source': 2, 'target': 1, 'command': '', 'response': '', 'value': 1}]

    >>> df = pd.DataFrame([['', '', '1', '2'], ['', '', '2', '3'], ['', '', '4', '5'], ['', '', '6', '7'], ['', '', '1|2', '7'], ['', '', '8', '2|3'], ['', '', '4|9', '9'], ['', '', '4|6', '3|5']], columns=('trigger', 'response', 'source_state', 'dest_state')) # noqa
    >>> gen_links(path=DATA_DIR, value=1, df=df)
    [{'source': 0, 'target': 1, 'command': '', 'response': '', 'value': 1},
     {'source': 1, 'target': 2, 'command': '', 'response': '', 'value': 1},
     {'source': 3, 'target': 4, 'command': '', 'response': '', 'value': 1},
     {'source': 5, 'target': 6, 'command': '', 'response': '', 'value': 1},
     {'source': 0, 'target': 6, 'command': '', 'response': '', 'value': 1},
     {'source': 1, 'target': 6, 'command': '', 'response': '', 'value': 1},
     {'source': 7, 'target': 1, 'command': '', 'response': '', 'value': 1},
     {'source': 7, 'target': 2, 'command': '', 'response': '', 'value': 1},
     {'source': 3, 'target': 8, 'command': '', 'response': '', 'value': 1},
     {'source': 3, 'target': 2, 'command': '', 'response': '', 'value': 1},
     {'source': 3, 'target': 4, 'command': '', 'response': '', 'value': 1},
     {'source': 5, 'target': 2, 'command': '', 'response': '', 'value': 1},
     {'source': 5, 'target': 4, 'command': '', 'response': '', 'value': 1}]


    """
    links = []
    node_names = get_nodes(DF=df)
    for source_index, source_name in enumerate(df.source_state.values):
        if not is_globstar(str(source_name)):
            current_dest_name = df.dest_state[source_index]
            if not is_globstar(str(current_dest_name)):
                links.append({'source': node_names.index(source_name),
                              'target': node_names.index(current_dest_name),
                              'command': df.trigger[source_index],
                              'response': df.response[source_index],
                              'value': value})
            else:
                dest_pattern = pattern.expand_globstar(current_dest_name)
                for dest_index, dest_name in enumerate(df.dest_state.values):
                    if regex.match(dest_pattern, dest_name) and not is_globstar(dest_name):
                        links.append({'source': node_names.index(source_name),
                                      'target': node_names.index(dest_name),
                                      'command': df.trigger[source_index],
                                      'response': df.response[dest_index],
                                      'value': value})
        else:
            if not is_globstar(df.dest_state[source_index]):
                current_dest_name = df.dest_state[source_index]
                source_pattern = pattern.expand_globstar(source_name)
                for source_index, source_name in enumerate(df.source_state.values):
                    if regex.match(source_pattern, source_name) and not is_globstar(source_name):
                        links.append({'source': node_names.index(source_name),
                                      'target': node_names.index(current_dest_name),
                                      'command': df.trigger[source_index],
                                      'response': df.response[source_index],
                                      'value': value})
            else:
                source_pattern = pattern.expand_globstar(source_name)
                current_dest_name = df.dest_state[source_index]
                dest_pattern = pattern.expand_globstar(current_dest_name)
                for current_source_index, current_source_name in enumerate(node_names):
                    if regex.match(source_pattern, current_source_name) and not is_globstar(current_source_name):
                        for dest_index, dest_name in enumerate(node_names):
                            if regex.match(dest_pattern, dest_name) and not is_globstar(dest_name):
                                links.append({'source': node_names.index(current_source_name),
                                              'target': node_names.index(dest_name),
                                              'command': df.trigger[source_index],
                                              'response': df.response[source_index],
                                              'value': value})
    return links


def create_json(path=DATA_DIR):
    dialog = dialog_graph.base_dialog()
    dialog['nodes'] = gen_nodes()
    dialog['links'] = gen_links()
    js = json.dumps(dialog, indent=2)
    with open("../data/newdialog.json", "w") as f:
        f.write(js)
    return js


if __name__ == "__main__":
    df = load_df()
