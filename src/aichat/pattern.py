""" Statement->response mappings to select best response template for any statement """
import regex
import logging

try:
    import exrex
except ImportError:
    class exrex:
        def getone(s):
            return s

REGEX_ALIASES = {
    r'\w': r'a-zA-Z_',
    r'\s': r'\t\r\n\ ',
    # r'\W': r'^a-zA-Z_',
    # r'\S': r'^\t\r\n\ ',
    }

logger = logging.getLogger(__name__)


def expand_charclass(patt, alias=r'\w', expansion=None):
    r""" Translate a single character class shortcut into its full explicit square-bracket form

    >>> expand_charclass(patt=r'[\w\r\s]*', alias=r'\w', expansion=r'a-zA-Z_')
    '[a-zA-Z_\\r\\s]*'

    FIXME:
      Fails on multiple square-bracketed character classes
      Fails on square-bracketed character classes that include or exclude literal square brackets
    """
    # patt = patt.replace('[ ]', r'\ ')
    if expansion is None:
        expansion = REGEX_ALIASES[alias]
    patt = patt.replace(alias, '[' + expansion + ']')
    # clean up any nested square-brackets
    patt = regex.sub(r'(.*)\[([^\[\]]*)\[' + expansion + r'\](.*)\](.*)', r'\1[\2' + expansion + r'\3]\4', patt)
    return patt


def expand_pattern(patt):
    r""" Expand regular expression character class aliases like \w and \s for FSM generators like exrex

    >>> expand_pattern(r'Hello\ [\w\s]*') == 'Hello\\ [a-zA-Z_[\\t\\r\\n\\ ]]*'
    True

    FIXME:
      Correctly expand all character classes, not just \s and \w
    """
    # patt = patt.replace('[ ]', r'\ ')
    for alias in REGEX_ALIASES:
        patt = expand_charclass(patt, alias)
    return patt


def truncate_pattern(patt, star_len=10, plus_len=None):
    r""" Replace Kleine '*' and '+' regex quantifiers with {star_len} so that FSM generators like exrex terminate

    >>> truncate_pattern(r'(Hello)+ [\w\s]*') == '(Hello){10} [\\w\\s]{10}'
    True
    >>> truncate_pattern(r'(Hello)+ [\w\s]*', 8) == '(Hello){8} [\\w\\s]{8}'
    True
    >>> truncate_pattern(r'(Hello)+ [\w\s]*', 2, 3) == '(Hello){3} [\\w\\s]{2}'
    True
    """
    star_len = int(star_len)
    if star_len > 1000000:
        logger.warn("That's a REALY BIG Kleine star (*)." +
                    "Do you really want {}-char strings in your language?".format(star_len))
    if plus_len is None:
        plus_len = star_len
    else:
        plus_len = int(plus_len)
        if plus_len > 1000000:
            logger.warn("That's a REALY BIG Kleine plus (+)." +
                        "Do you really want {}-char strings in your language?".format(plus_len))
    star_len, plus_len = str(star_len), str(plus_len)
    patt = regex.sub(r'([^\\])\*', r'\1{' + star_len + r'}', patt)
    patt = regex.sub(r'([^\\])\+', r'\1{' + plus_len + r'}', patt)
    return patt


def exrex_pattern(patt, star_len=10, plus_len=None):
    r""" truncate_pattern(expand_pattern(patt)) to help exrex patt generator

    >>> exrex_pattern(r'Hello\ [\w]*', 23) == 'Hello\\ [a-zA-Z_]{23}'
    True
    """
    if plus_len is None:
        plus_len = star_len
    return truncate_pattern(expand_pattern(patt), star_len=star_len, plus_len=plus_len)


def regex_len(patt, star_len=10, plus_len=None):
    r""" Calculate the approximate minimum length of a str that will match the given regex (# states of FSM)

    >>> 30 <= regex_len(r'([\w]{7}\s{1}\w?[0-9]{2})*', 3) <= 33
    True
    """
    if plus_len is None:
        plus_len = star_len
    patt = getattr(patt, 'pattern', patt)
    # return len(patt)
    return len(exrex.getone(exrex_pattern(patt, star_len=star_len, plus_len=plus_len)))


RESPONSE_MAPPING = [('Hi', 'Hi!'), ("Hi", "Hi, I'm Bot")]
CONTEXT = {}


def compile_pattern(patt, fuzziness=1, **kwargs):
    r""" Compile a Bot Language Pattern (glob star or AIML syntax) into a python regular experssion object

    Args:
      patt (str): glob star pattern, regular expression pattern, or fixed string (exact match)

    Returns:
      compiled regex object if patt contains _, +, *, #, or | characters
      str for fixed string patterns (only letters, spaces and natural English punctuation

    >>> compile_pattern("Hello|Hi *").match("Hi world")
    <regex.Match object; span=(0, 4), match='Hi w', fuzzy_counts=(1, 0, 0)>
    >>> compile_pattern("Hello World!")
    'Hello World!'
    """
    fuzziness = 3 if fuzziness is True else int(fuzziness) if fuzziness is not None else fuzziness
    if isinstance(fuzziness, float) and 0 < fuzziness < 1:
        fuzziness = int(round(fuzziness * regex_len(patt), 0))
    if next(regex.finditer(r'[[*#{\\]', patt), None):
        # r'{' in patt or r'[' in patt or '\\' or r'*' in patt or r'#' in patt:
        if fuzziness:
            patt = '(' + patt + '){e<=' + str(fuzziness) + '}'
        if r'{' in patt or r'[' in patt or '\\' in patt:
            return regex.compile(patt, **kwargs)
        if r'*' in patt or r'#' in patt:
            patt.replace(r'*', r'[-a-zA-Z]+')
            patt.replace(r'#', r'([-a-zA-Z]+[ ]{0,1})+')
            patt.replace(r' ', r'[ ]')
            patt.replace(r'[[ ]]', r'[ ]')  # undo redundant brackets
            patt.replace(r'[[ ]]', r'[ ]')  # undo tripply redundant brackets
            return regex.compile(patt, **kwargs)
    else:
        return patt


def remove_punc(s: str):
    r""" Replace all nondigit-nonword characters with spaces and delete meaningless spaces

    >>> remove_punc('<"hyphenated-word {variable}!!?">')  # doctest.NORMALIZE_WHITESPACE
    'hyphenated word variable'
    """
    s = regex.sub(r'[^a-zA-Z0-9]', ' ', s).strip()
    s = ' '.join([tok.strip() for tok in s.split() if tok])
    return s


class PatternMap:
    r""" Like a dict, but with locality-sensitive hashes of keys, fuzzy regex keys, and redundant keys

    Methods:
      __getitem__(str): returns a list of str templates

    Attributes:
      .exact_strs: {
        str1: [response_template1_1, response_template1_2, ...],
        str2: [response_template2_1, response_template2_2, ...],
        ...
        }
      .patterns: {
        pattern_str1: (compiled_pattern1, [response_template1_1, response_template1_2, ...]),
        pattern_str2: (compiled_pattern2, [response_template2_2, response_template2_2, ...]),
        ...
        }

    >>> responses = PatternMap([('Hey', 'Hi!'), ('Hello *', 'Bye!'), ('Hey|Hello #', 'WAT?')])
    >>> responses['Hey']
    ['Hi!']
    >>> responses['Hello World!']
    ['Bye!']
    >>> responses['Hello World What are you up to?']
    ['Bye!']
    >>> responses['Hey World What are you up to?']
    ['WAT?']
    >>> responses['Hey Joe,']
    ['WAT?']
    >>> len(responses.patterns)
    2
    """

    def __init__(self, mapping=None, case_sensitive=False, fuzziness=1):
        self.case_sensitive = case_sensitive
        self.fuzziness = fuzziness
        self.exact_strs = {}
        self.patterns = {}
        self.learn(mapping)

    # TODO: rename `update()`?
    def learn(self, mapping=None):
        """ Assumes that all regex keys in the mapping have been compiled into regex objects """
        mapping = [] if mapping is None else mapping
        for pattern_template in mapping:
            if pattern_template is None:
                continue
            patt, template = pattern_template[0], pattern_template[1]
            patt = compile_pattern(patt)
            if isinstance(patt, str):
                self.exact_strs[patt] = self.exact_strs.get(patt, []) + [template]
                lowered_patt = patt.lower()
                # print(lowered_patt, template)
                if lowered_patt != patt:
                    self.exact_strs[patt.lower()] = self.exact_strs.get(lowered_patt, []) + [template]
                normalized_patt = remove_punc(lowered_patt)
                # print(normalized_patt, template)
                if normalized_patt not in (patt, lowered_patt):
                    self.exact_strs[normalized_patt] = self.exact_strs.get(normalized_patt, []) + [template]
            else:
                self.patterns[patt.pattern] = (
                    patt, self.patterns.get(patt.pattern, (patt, []))[1] + [template])

    def __getitem__(self, statement):
        """ Returns a list of possible resonse templates based on a statement==pattern match """
        if statement in self.exact_strs:
            return self.exact_strs[statement]
        for (pattern_str, (patt, templates)) in zip(self.patterns.keys(), self.patterns.values()):
            if patt.match(statement):
                return templates
        return []

    def __str__(self):
        return str({'patterns': self.patterns, 'exact_strs': self.exact_strs})

    def __repr__(self):
        return self.__class__.__name__ + '<' + str({'patterns': self.patterns, 'exact_strs': self.exact_strs}) + '>'


class CallbackDict(dict):
    r""" A dictionary that will attempt to call the callback in value before returning the bare value

    References:
      https://stackoverflow.com/a/46106852/623735
    """

    def __getitem__(self, key):
        value = super().__getitem__(key)
        try:
            return value(key)
        except TypeError:
            try:
                return value()
            except TypeError:
                return value


class Responder:
    """ See PatternMap class for a better approach """

    def __init__(
            self, on_say=print, response_mapping=None, context=None,
            ignore_case=True, ignore_punc=True):
        self.response_mapping = response_mapping or RESPONSE_MAPPING
        self.on_say = on_say
        self.context = context or CONTEXT
        self.ignore_case = ignore_case
        self.ignore_punc = ignore_punc

    def say(self, s):
        self.on_say(s)
        return s

    def find_responses(self, statement):
        """ Return templates whose patterns match the provided statement (user utterance)

        Args:
            statement (str): The user statement including capitalizaiton and punctuation
        Returns:
            [str]: The bot responses associated with the patterns that match the user statement
        """
        responses = []
        # O(N) algorithm must be improved with a pattern match search index or semantic search index like annoy
        for patt, template in self.response_mapping:
            match = None
            try:
                match = patt.match(statement)
            except AttributeError:
                if self.ignore_case:
                    patt = patt.lower()
                if self.ignore_punc:
                    patt = remove_punc(patt)
                if patt == statement:
                    match = True
            if match:
                responses.append(template)
        return [r for (s, r) in self.response_mapping if s == statement]

    def respond(self, statement, min_confidence=0):
        """ Reply with the best response that meets the min confidence threshold """
        responses = self.find_responses(statement)
        resp = responses[0]
        self.say(resp)
