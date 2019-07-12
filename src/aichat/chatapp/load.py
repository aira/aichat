import os

import pandas as pd

from aichat.chatsite.settings import CSV_DEFAULT_PATH, CSV_COLUMNS
from .models import TriggerResponse


def load(path=CSV_DEFAULT_PATH, allow_dupes=True):
    numrecords = TriggerResponse.objects.count()
    df = pd.read_csv(path, header=None)
    columns = list(df.columns) + 'source dest'.split()
    for i in range(len(df.columns), 4):
        df[columns[i]] = pd.np.nan

    df = df.fillna('root')  # new
    df.columns = CSV_COLUMNS[:len(df.columns)]
    create = TriggerResponse.objects.create if allow_dupes else TriggerResponse.objects.get_or_create
    for i, row in df.iterrows():
        create(**row)

    numadded = TriggerResponse.objects.count() - numrecords
    return numadded


def load_all(path=os.path.dirname(CSV_DEFAULT_PATH), allow_dupes=True):
    numadded = {}
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isfile(filepath) and filename.lower().endswith('.csv'):
            numadded[filename] = load(filepath, allow_dupes=allow_dupes)
    return numadded


def test_load(path=os.path.dirname(CSV_DEFAULT_PATH), allow_dupes=True):
    numadded = {}
    total = 0
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isfile(filepath) and filename.lower().endswith('.csv'):

            numadded[filename] = load(filepath, allow_dupes=allow_dupes)
            df = pd.read_csv(filepath, header=None)
            total += len(df)
            print(filepath)
            assert(total == TriggerResponse.objects.count())
    return numadded
