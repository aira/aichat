import os
import json
import typing
from vocabulary.vocabulary import Vocabulary as vb
import object_detection.constants as const

CLASS_SYNONYM_DICT = None
NLP_DIR = os.path.abspath(os.path.dirname(__file__))
CLASS_SYNONYM_FILE = NLP_DIR.rstrip('/') + '/class_synonyms.json'


def build_synonym_dict(filename: str = CLASS_SYNONYM_FILE, force=False) -> None:

    if os.path.exists(filename) and not force:
        return

    display_names = []
    with open(const.PATH_TO_LABELS, 'r') as label_file:
        for line in label_file.readlines():
            if 'display_name' in line:
                display_names.append(line.split(':')[-1].replace('"', '').strip())

    word_assoc = {}

    for name in display_names:
        syn_list = get_synonym_list(name)

        # Identity
        word_assoc[name] = name

        # Association lookup
        for syn in syn_list:

            word_assoc[syn] = name

    with open(filename, 'w') as dest_file:
        json.dump(word_assoc, dest_file)


def get_synonym_list(source_word: str) -> typing.List[str]:
    syn_json = vb.synonym(source_word)

    if not syn_json:
        return list()

    syn_dicts = json.loads(syn_json)

    return [syn_dict['text'].replace('"', '') for syn_dict in syn_dicts]


build_synonym_dict()


def load(filename: str = CLASS_SYNONYM_FILE) -> typing.Dict[str, str]:
    with open(filename, 'r') as file:
        return json.load(file)


def synonym_to_label(syn: str) -> typing.Optional[str]:
    global CLASS_SYNONYM_DICT

    if CLASS_SYNONYM_DICT is None:
        CLASS_SYNONYM_DICT = load()

    return CLASS_SYNONYM_DICT.get(syn, None)


def are_synonyms(source, target):
    global CLASS_SYNONYM_DICT

    if CLASS_SYNONYM_DICT is None:
        CLASS_SYNONYM_DICT = load()

    if CLASS_SYNONYM_DICT.get(source, -1) == CLASS_SYNONYM_DICT.get(target, -2):
        return True

    return False
