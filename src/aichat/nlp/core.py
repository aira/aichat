""" Natural Language Processing (Generation) utilities """
import os
import typing

import pandas as pd
import object_detection.constants as constants

# TODO fix the antipattern of having a separate folder for every function/class
from object_detection.color.labeler import estimate_color
from nlp.plurals import PLURALS
from nlp.transform import position, estimate_distance

from collections import Counter
from object_detection.constants import logging
# from object_detection import db

logger = logging.getLogger('object_detector')


def pluralize(s):
    """ Convert word to its plural form.

    >>> pluralize('cat')
    'cats'
    >>> pluralize('doggy')
    'doggies'

    Better:

    >> from pattern.en import pluralize, singularize

    Or, even better, just create pluralized versions of all the class names by hand!
    """
    word = str.lower(s)
    # `.get()` rather than `word in PLURALS` so that we only look up the word once
    pluralized_word = PLURALS.get(word, None)
    if pluralized_word is not None:
        return pluralized_word

    # case = str.lower(s[-1]) == s[-1]
    if word.endswith('y'):
        if word.endswith('ey'):
            return word + 's'
        else:
            return word[:-1] + 'ies'
    elif word[-1] in 'sx' or word[-2:] in ['sh', 'ch']:
        return word + 'es'
    elif word.endswith('an') and len(word) > 3:
        return word[:-2] + 'en'
    else:
        return word + 's'


def update_state(image, boxes, classes, scores, category_index, window=10, max_boxes_to_draw=None, min_score_thresh=.5):
    """ Revise state based on latest frame of information (object boxes)

    Args:
        boxes (list): 2D numpy array of shape (N, 4): (ymin, xmin, ymax, xmax), in normalized format between [0, 1].
        classes,
    Args (that should be class attributes):
        category_index (dict of dicts): {1: {'id': 1, 'name': 'person'}, 2: {'id': 2, 'name': 'bicycle'},...}
    Returns:
        list: list of object vectors, (see `constants.py` for definition)
    """
    object_vectors = []

    pass_thresh = [(label, score, bbox) for (label, score, bbox) in zip(classes, scores, boxes)
                   if score >= min_score_thresh]

    for label, score, bbox in pass_thresh:

        class_name = category_index.get(label, {'name': 'unknown object'})['name']
        new_score = score

        display_str = '{}: {} {}%'.format(label, class_name, int(100 * score))
        logger.info(display_str)

        label_series = pd.Series([class_name, 0, new_score], index=constants.LABEL_KEYS)
        bbox_series = pd.Series(estimate_distance(bbox), index=constants.BB_KEYS)
        color_series = estimate_color(image, box=bbox)

        all_series = [label_series, bbox_series, color_series]

        state = pd.concat(all_series)

        object_vectors.append(constants.ObjectSeries(state, index=constants.OBJECT_VECTOR_KEYS))

    return object_vectors


def describe_scene(object_vectors, min_conf=constants.MIN_CONF_THRESH):
    """ Convert a state vector dictionary of objects and their counts into a natural language string

            categ inst,  conf, x   y  z  wdth hght dpth blk wht red orng  yel  grn  cyn  blu purp pink
    >>> object_vectors = [
    ...    ['cup', 0, .95, -.5, .1, 0, .1, .1, 0, .5, .3, .14, .01, .01, .01, .01, .01, .01, .01, 0.1, 0.1,
    ...      0.1, 0.1, 0.1, 0.1],
    ...    ['cup', 0,   .95, -.5, .1, 0,  .1,  .1,  0,  .5, .3, .14, .01, .01, .01, .01, .01, .01, .01, 0.1, 0.1,
    ...     0.1, 0.1, 0.1, 0.1],
    ...    ['ski', 0,   .80, -.5, .1, 0,  .1,  .1,  0, .5, .3, .14, .01, .01, .01, .01, .01, .01, .01, 0.1, 0.1,
    ...     0.1, 0.1, 0.1, 0.1 ]
    ... ]
    >>> desc = describe_scene(object_vectors, min_conf=0.75)
    >>> '2 black cups' in desc and ' and ' in desc and 'a black ski' in desc
    True
    >>> conf_desc = describe_scene(object_vectors, min_conf=0.9)
    >>> '2 black cups' in conf_desc and 'and' not in conf_desc and 'a black ski' not in conf_desc
    True
    >>> describe_scene(object_vectors, min_conf=.99)
    ''
    """
    conf_object_vectors = filter(lambda vec: vec[2] >= min_conf, object_vectors)

    feature_list = list(map(object_features, conf_object_vectors))

    plural_descriptions = aggregate_descriptions_by_features(feature_list)

    delim_description = compose_comma_series(plural_descriptions)

    return delim_description


def count_scene(object_vectors, min_conf=constants.MIN_CONF_THRESH):

    conf_object_vectors = filter(lambda vec: vec[2] >= min_conf, object_vectors)

    feature_list = list(map(object_features, conf_object_vectors))

    plural_descriptions = aggregate_descriptions_by_features(feature_list, use_articles=False,
                                                             include_position=False, include_color=False)

    delim_description = compose_comma_series(plural_descriptions)

    return delim_description


def aggregate_descriptions_by_features(feature_list, *,
                                       use_articles: bool = True,
                                       include_color: bool = True, include_position: bool = True) -> typing.List[str]:
    """Produce a list of descriptions created through aggregations (counts) of objects in the scene.

    Can optionally aggregate by color and position.

    Args:
        feature_list: list of tuples with description features [(<category name>, <color>, <position>), ...]
        use_articles: flag to use articles vs the number 1 to describe a single object
        include_color: flag to aggregate by color
        include_position: flag to aggregate by position

    Returns:
        A list of strings with valid descriptions.

    Examples:
        TODO(Hobbs, Ashwin): Please review these test cases
        >>> obj_vectors = [
        ...    ['cup', 0, .95, -.5, .1, 0, .1, .1, 0, .5, .3, .14, .01, .01, .01, .01, .01, .01, .01, 0.1, 0.1,
        ...      0.1, 0.1, 0.1, 0.1],
        ...    ['cup', 0,   .95, -.5, .1, 0,  .1,  .1,  0,  .5, .3, .14, .01, .01, .01, .01, .01, .01, .01, 0.1, 0.1,
        ...     0.1, 0.1, 0.1, 0.1],
        ...    ['ski', 0,   .80, -.5, .1, 0,  .1,  .1,  0, .5, .3, .14, .01, .01, .01, .01, .01, .01, .01, 0.1, 0.1,
        ...     0.1, 0.1, 0.1, 0.1]
        ... ]
        >>> feature_list = list(map(object_features, obj_vectors))
        >>> descs = aggregate_descriptions_by_features(feature_list)
        >>> '2 black cups to your left' in descs and 'a black ski to your left' in descs
        True
        >>> no_color = aggregate_descriptions_by_features(feature_list, include_color=False)
        >>> '2 cups to your left' in no_color and 'a ski to your left' in no_color
        True
        >>> obj_vectors_color = [
        ...    ['cup', 0, .95, -.5, .1, 0, .1, .1, 0, .5, .3, .14, .01, .51, .01, .01, .01, .01, .01, 0.1, 0.1,
        ...      0.1, 0.1, 0.1, 0.1],
        ...    ['cup', 0,   .95, -.5, .1, 0,  .1,  .1,  0,  .5, .3, .14, .01, .01, .01, .01, .01, .01, .01, 0.1, 0.1,
        ...     0.1, 0.1, 0.1, 0.1],
        ...    ['ski', 0,   .80, -.5, .1, 0,  .1,  .1,  0, .5, .3, .14, .01, .01, .01, .01, .01, .01, .01, 0.1, 0.1,
        ...     0.1, 0.1, 0.1, 0.1]
        ... ]
        >>> feature_list = list(map(object_features, obj_vectors_color))
        >>> diff_colors = aggregate_descriptions_by_features(feature_list)
        >>> 'a dark blue cup to your left' in diff_colors and 'a black cup to your left' in diff_colors
        True
        >>> diff_no_colors = aggregate_descriptions_by_features(feature_list, include_color=False)
        >>> '2 cups to your left' in diff_no_colors
        True
        >>> obj_vectors_pos = [
        ...    ['cup', 0, .95, 0.7, .1, 0, .1, .1, 0, .5, .3, .14, .01, .01, .01, .01, .01, .01, .01, 0.1, 0.1,
        ...      0.1, 0.1, 0.1, 0.1],
        ...    ['cup', 0,   .95, -.5, .1, 0,  .1,  .1,  0,  .5, .3, .14, .01, .01, .01, .01, .01, .01, .01, 0.1, 0.1,
        ...     0.1, 0.1, 0.1, 0.1],
        ...    ['ski', 0,   .80, -.5, .1, 0,  .1,  .1,  0, .5, .3, .14, .01, .01, .01, .01, .01, .01, .01, 0.1, 0.1,
        ...     0.1, 0.1, 0.1, 0.1]
        ... ]
        >>> feature_list = list(map(object_features, obj_vectors_pos))
        >>> diff_pos = aggregate_descriptions_by_features(feature_list)
        >>> 'a black cup to your left' in diff_pos and 'a black cup to your right' in diff_pos
        True
        >>> diff_no_pos = aggregate_descriptions_by_features(feature_list, include_position=False)
        >>> '2 black cups' in diff_no_pos
        True
    """

    def include_features(f):
        """Filters feature tuple s.t. we include only the features we want to aggregate over. """
        assert len(f) == 3, 'Make sure to include all the features in this function!!'

        fs = list()
        fs.append(f[0])

        if include_color:
            fs.append(f[1])

        if include_position:
            fs.append(f[2])

        return tuple(fs)

    included = list(map(include_features, feature_list))

    counts = Counter(included)

    pluralized_feature_groups = [describe_object_from_feature(feature, count,
                                                              use_articles=use_articles,
                                                              include_color=include_color,
                                                              include_position=include_position)
                                 for feature, count in counts.items()]

    return pluralized_feature_groups


def describe_object(obj_vec) -> str:
    """Creates formatted string description from object vector

    Args:
        obj_vec: a vector representing a single object.

    Returns:
        a description of the object.

    Examples:

        >>> obj_vec = ['cup', 0,   .95, -.5, .1, 0,  .1,  .1,  0, .5, .3, .14, .01, .01, .01, .01, .01, .01, .01, 0.1, \
                       0.1, 0.1, 0.1, 0.1, 0.1]
        >>> describe_object(obj_vec)
        'a black cup to your left'
    """
    feature = object_features(obj_vec)
    return describe_object_from_feature(feature)


def describe_object_from_feature(feature, count: typing.Optional[int] = None, *,
                                 use_articles: bool = True,
                                 include_color: bool = True, include_position: bool = True) -> str:
    """Creates formatted string description from object features and counts, including pluralization.

    Args:
        feature (3-tuple of str): (category, color, location)
        count (int): a count of the occurrence of the feature, or None
        use_articles (bool): Optionally use articles or 1 to describe a single object
        include_color (bool): Optionally include the color feature in description
        include_position (bool): Optionally include the position in object description

    Returns:
        A noun phrase describing the object.

    >>> describe_object_from_feature(('cup', 'white', 'left'))
    'a white cup to your left'
    >>> describe_object_from_feature(('cup', 'orange', 'center'))
    'an orange cup to your center'
    >>> describe_object_from_feature(('person', 'orange', 'center'))
    'a person wearing mostly orange to your center'
    >>> describe_object_from_feature(('cup', 'red', 'right'), 2)
    '2 red cups to your right'
    >>> describe_object_from_feature(('cup', 'red', 'right'), 2)
    '2 red cups to your right'
    >>> describe_object_from_feature(('cup', 'blue','right'), 1, use_articles=False)
    '1 blue cup to your right'
    >>> describe_object_from_feature(('cup', 'right'), 1, include_color=False)
    'a cup to your right'
    >>> describe_object_from_feature(('cup', 'blue'), 1, include_position=False)
    'a blue cup'
    >>> describe_object_from_feature(('cup',), 1,  use_articles=False, include_color=False, include_position=False)
    '1 cup'

    Raises:
        - AssertionError: This is for development time. Should the feature tuple get more than
            the expected number of items in the tuple, an assertion error should be thrown
        - ValueError: Count cannot be zero, negative, or an non-integer less than 1.

    """
    name, *rest = feature

    if include_color:
        color, *rest = rest
    else:
        color = None

    if include_position:
        position, *rest = rest
    else:
        position = None

    assert len(rest) == 0, 'Need to update string formatting function with new features!'

    if count is None:
        count = 1

    # Structure the string templates based on what features to include
    template = '{name}'

    if include_color:
        if name.lower().strip()[:2] in ['pe']:  # TODO: this is too general of logic. Only cover 'people*' and 'person*'
            template = template + ' wearing mostly {color}'
        else:
            template = '{color} ' + template

    if include_position:
        template = template + ' to your {position}'

    template = '{amount} ' + template

    output = template.format(amount=str(count) if count > 1 else '',
                             color=color,
                             name=pluralize(name) if count > 1 else name,
                             position=position)

    if count == 1:
        if use_articles:
            output = ('an' if _starts_with_vowel(output.split()[0]) else 'a') + output
        else:
            output = '1' + output

    return output


def _starts_with_vowel(char) -> bool:
    """Test to see if string starts with a vowel

    Args:
        char: character or string

    Returns:
        bool True if the character is a vowel, False otherwise

    Examples:
        >>> _starts_with_vowel('a')
        True
        >>> _starts_with_vowel('b')
        False
        >>> _starts_with_vowel('cat')
        False
        >>> _starts_with_vowel('apple')
        True
    """
    if len(char) > 1:
        char = char[0]

    return char in 'aeiou'


def object_features(obj_vec):
    """Converts object vector to a tuple of labels (name, color, position, etc.)

    Args:
        obj_vec:

    Returns:
        Tuple of strings with the following format:
        (<cateogry name>, <color>, ...)

    Examples:
        >>> obj_vec = ['cup', 0, .95, -.5, .1, 0, .1, .1, 0, .5, .3, .14, .01, .01, .01, .01, .01, .01, .01, 0.1, 0.1,\
                       0.1, 0.1, 0.1, 0.1]
        >>> object_features(obj_vec)
        ('cup', 'black', 'left')
    """
    if type(obj_vec) is list or type(obj_vec) is pd.Series:
        obj_vec = constants.ObjectSeries(obj_vec, index=constants.ObjectSeries.OBJECT_VECTOR_KEYS)

    #       Name,                Color,                    Position
    return obj_vec['category'], obj_vec.obj_primary_color, position(tuple(obj_vec.obj_bbox))


def compose_comma_series(noun_list: typing.List[str]) -> str:
    """ Join a list of noun phrases into a comma delimited series

    Args:
        noun_list: list of noun phrases (object + adjective descriptors)

    Returns:
        string consisting of a comma delimited series of noun phrases

    Examples:
        >>> compose_comma_series(['1 pair of skis', '2 cups'])
        '1 pair of skis and 2 cups'
        >>> compose_comma_series(['1 pair of skis', '2 cups', '1 laptop'])
        '1 pair of skis, 2 cups and 1 laptop'
    """
    comma_list = ', '.join(noun_list[:-2])
    conjunction = ' and '.join(noun_list[-2:])

    if len(comma_list) > 0:
        delim_description = comma_list + ', ' + conjunction
    else:
        delim_description = conjunction

    return delim_description


def say(s, rate=250):
    """ Convert text to speech (TTS) and play resulting audio to speakers

    If "say" command is not available in os.system then print the text to stdout and return False.

    >>> result = say('hello')  # TODO(Ashwin | Alex | Hobbs) This test will fail on Jenkins
    >>> result == 'hello' or result == False
    True
    """
    shell_cmd = 'say --rate={rate} "{s}"'.format(**dict(rate=rate, s=s))
    try:
        status = os.system(shell_cmd)
        if status > 0:
            logger.error('os.system({shell_cmd}) returned nonzero status: {status}'.format(**locals()))
            raise OSError
        return s
    except OSError:
        logger.error(s)
    return False
