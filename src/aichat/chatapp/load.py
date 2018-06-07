import os

from pandas import read_csv

from aichat.chatsite.settings import CSV_DEFAULT_PATH, CSV_COLUMNS
from .models import TriggerResponse


def load(path=CSV_DEFAULT_PATH, allow_dupes=True):
    numrecords = TriggerResponse.objects.count()
    df = read_csv(path, header=None)
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
