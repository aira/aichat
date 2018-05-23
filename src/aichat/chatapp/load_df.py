from __future__ import print_function
import os
import json
import pandas as pd
import dialog_graph
import regex
from aichat import pattern

# from aichat.chatapp import dialog_graph
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
    node_list = list(set(DF.dest_state.fillna('root')))
    dict_list = []
    node_index = 0
    for node in node_list:
        # if '*' not in node and '?' not in node and '|' not in node:
        dict_list.append(
            {'name': node, 'id': 'node' + str(node_index)})
        node_index = node_index + 1
    return dict_list


def links_to_list(path=DATA_DIR, value=1):
    # links = []
    # source_list = DF.source_state
    # dest_list = DF.dest_state
    # nodes = nodes_to_list()
    # nodes_index = {}
    # for node_name in nodes:
    #     nodes_index[node_name['name']] = node_name['id'].replace('node', '')
    # for i, source in enumerate(source_list):
    #     patt = pattern.expand_globstar(source)
    #     for j, dest in enumerate(dest_list):
    #         match = regex.match(patt, dest)
    #         if match:
    #             # if int(nodes_index[source]) == int(nodes_index[dest]):
    #             #     continue
    #             links.append({'source': int(nodes_index[source]),
    #                           'target': int(nodes_index[dest]),
    #                           'command': DF.trigger[j],
    #                           'response': DF.response[j],
    #                           'value': value})
    # return links
    links = []
    node_names = list(set(DF.dest_state))  # list of node names (states)
    # print(nodes_index)
    for i, source_pattern in enumerate(DF.source_state.values):
        patt = pattern.expand_globstar(source_pattern)
        for j, name in enumerate(node_names):
            if ('{' in patt or '[' in patt) and regex.match(patt, name):
                print(str(j) + source_pattern + ',' + name)
                links.append({'source': node_names.index(name),
                              'target': node_names.index(DF.dest_state.values[i]),
                              'command': DF.trigger[i],
                              'response': DF.response[i],
                              'value': value})
            elif source_pattern == name:
                print("nonpattern:" + str(j) + source_pattern + ',' + name)
                links.append({'source': node_names.index(name),
                              'target': node_names.index(DF.dest_state.values[i]),
                              'command': DF.trigger[i],
                              'response': DF.response[i],
                              'value': value})

    return links


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
