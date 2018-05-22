from __future__ import print_function
import os
import json
import pandas as pd
import dialog_graph
import regex
from tqdm import tqdm
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
    df_clean = df_clean.fillna('')
    return df_clean


DF = load_df()


def nodes_to_list(path=DATA_DIR):
    state_list = DF.source_state
    dest_state = DF.dest_state
    node_list = state_list + dest_state
    node_list = list(set(node_list))
    dict_list = []
    for node in range(len(node_list)):
        dict_list.append({'name': node_list[node], 'id': 'node' + str(node)})
    return dict_list


def links_to_list(path=DATA_DIR, value=1):
    links = []
    source_list = DF.source_state
    dest_list = DF.dest_state
    for i, source in enumerate(source_list):
        for j, dest in enumerate(dest_list):
            patt = pattern.expand_globstar(source)
            match = regex.match(patt, dest)
            if match:
                links.append({'source': i,
                              'target': j,
                              'command': DF.trigger[i],
                              'response': DF.response[i],
                              'value': value})
    return links


def create_json(path=DATA_DIR):
    node_list = nodes_to_list(path)
    links_list = links_to_list()
    dialog = dialog_graph.base_dialog()
    dialog['nodes'] = node_list
    dialog['links'] = links_list
    js = json.dumps(dialog, indent=2)
    with open("../data/dialog.json", "w") as f:
        f.write(js)
    return js


if __name__ == "__main__":
    df = load_df()
