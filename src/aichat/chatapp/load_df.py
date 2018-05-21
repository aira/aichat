from __future__ import print_function
import os
import json
import pandas as pd
import dialog_graph
import sys

from aichat.chatapp import dialog_graph
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
                df = df.append(dfadd, sort=False)

    df_clean = pd.DataFrame(columns=CSV_COLUMNS, index=None)
    for column in CSV_COLUMNS:
        df_clean[column] = df[column]
    df_clean.to_csv("Export.csv", index=None)
    df_clean = df_clean.reset_index(drop=True)
    df_clean = df_clean.fillna('')
    return df_clean


def nodes_to_list(path='/Users/rigom/src/aichat/src/aichat/chatapp/data'):
    state_list = states_to_list('source_state')
    dest_state = states_to_list('dest_state')
    node_list = state_list + dest_state
    node_list = list(set(node_list))
    dict_list = []
    for node in range(len(node_list)):
        dict_list.append({'name': node_list[node], 'id': 'node' + str(node)})
    return dict_list


def states_to_list(state, path=DATA_DIR):
    state_list = []
    df = load_df(path)
    if state == 'source_state':
        state_list = list(set(df.source_state))
    elif state == 'dest_state':
        state_list = list(set(df.dest_state))
    elif state == 'response':
        state_list = list(df.response)
    elif state == 'trigger':
        state_list = list(df.trigger)
    return state_list


def nodes_to_dict(path=DATA_DIR):
    state_list = states_to_list('source_state')
    dest_state = states_to_list('dest_state')
    node_list = state_list + dest_state
    node_list = list(set(node_list))
    dict_list = []
    for node in range(len(node_list)):
        dict_list.append({'name:': node_list[node], 'id': 'node' + str(node)})
    return dict_list


def create_json(path='/Users/rigom/src/aichat/src/aichat/chatapp/data'):
    node_list = nodes_to_list(path)
    dialog = dialog_graph.base_dialog()
    dialog['nodes'] = node_list
    #dialog['nodes'][0]['name:'] = 'root'
    js = json.dumps(dialog, indent=2)
    with open("../data/newdialog.json", "w") as f:
        f.write(js)
    return js


def links_to_list(path=DATA_DIR):
    links = []
    trigger_list = states_to_list('trigger')
    response_list = states_to_list('response')
    for trig in range(len(trigger_list)):
        # get pattern from func
        for resp in range(len(response_list)):
            match = re.match(patt, response_list[resp])
            if match:
                links.append({'source': trig, 'target': resp,
                              'command': trigger_list[trig]['name:'], 'response': response_list[resp]['name:'], 'value': Fval})
    return links


def create_json(path=DATA_DIR):
    node_list = nodes_to_dict(path)
    dialog = dialog_graph.base_dialog()
    dialog['nodes'] = node_list
    dialog['nodes'][0]['name:'] = 'root'
    return dialog


if __name__ == "__main__":
    df = load_df()
