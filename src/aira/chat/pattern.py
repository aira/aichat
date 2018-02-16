""" Statement->response mappings to select best response template for any statement """
import regex
import logging

import exrex

logger = logging.getLogger(__name__)


def expand_pattern(pattern):
    """ Expand regular expression character class aliases like \w and \s for FSM generators like exrex

    >>> expand_pattern(r'Hello [\w\s]*')
    'Hello [a-zA-Z_\n\r\t ]*'

    FIXME:
      Correctly expand all character classes, not just \s and \w
    """
    pattern = regex.sub(r'(\[[^\]]*)\w([^\]]\])', pattern, r'\1a-zA-Z_\2')
    pattern = regex.sub(r'\w', pattern, r'[a-zA-Z_]')
    # FIXME: pattern = regex.sub(r'(\[[^\]]*)\W([^\]]\])', pattern, r'\1a-zA-Z_\2')
    pattern = regex.sub(r'\W', pattern, r'[^a-zA-Z_]')
    pattern = regex.sub(r'(\[[^\]]*)\s([^\]]\])', pattern, r'\1\n\r\t \2')
    pattern = regex.sub(r'\s', pattern, r'[\n\r\t ]')
    # FIXME: pattern = regex.sub(r'(\[[^\]]*)\s([^\]]\])', pattern, r'\1\n\r\t \2')
    pattern = regex.sub(r'\S', pattern, r'[^\n\r\t ]')
    return pattern


def truncate_pattern(pattern, star_len=10, plus_len=None):
    """ Replace Kleine '*' and '+' regex quantifiers with {star_len} so that FSM generators like exrex terminate

    >>> exrex_pattern(r'(Hello)+ [\w\s]*')
    '(Hello){10} [\w\s]{10}'
    >>> exrex_pattern(r'(Hello)+ [\w\s]*', 8)
    '(Hello){8} [\w\s]{8}'
    >>> exrex_pattern(r'(Hello)+ [\w\s]*', 2, 3)
    '(Hello){3} [\w\s]{2}'
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
    pattern = regex.sub(r'([^\])\*', pattern, '\1{' + star_len + '}')
    pattern = regex.sub(r'([^\])\+', pattern, '\1{' + plus_len + '}')
    return pattern


def exrex_pattern(pattern, star_len=10):
    """ truncate_pattern(expand_pattern(pattern)) to help exrex pattern generator

    >>> exrex_pattern(r'Hello [\w\s]*', 23)
    'Hello [a-zA-Z_\n\r\t ]{23}'
    """
    return truncate_pattern(expand_pattern(pattern))


def regex_len(pattern):
    """ Calculate the approximate minimum length of a str that will match the given regex (# states of FSM)

    >>> 30 <= regex_len(r'([\w\s]{7}[\s]{1}\w?[0-9]{2})*', 3) <= 33)
    True
    """
    pattern = getattr(pattern, 'pattern', pattern)
    # return len(pattern)
    return len(exrex.getone(exrex_pattern(pattern)))


RESPONSE_MAPPING = [('Hi', 'Hi!'), ("Hi", "Hi, I'm Bot")]
CONTEXT = {}


def compile_pattern(pattern, fuzziness=1, **kwargs):
    """ Compile a Bot Language Pattern (glob star or AIML syntax) into a python regular experssion object

    Args:
      pattern (str): glob star pattern, regular expression pattern, or fixed string (exact match)

    Returns:
      compiled regex object if pattern contains _, +, *, #, or | characters
      str for fixed string patterns (only letters, spaces and natural English punctuation

    >>> compile_pattern("Hello|Hi *").match("Hi world")
    <re.match ...>
    """
    fuzziness = 3 if fuzziness is True else int(fuzziness) if fuzziness is not None else fuzziness
    if isinstance(fuzziness, float) and 0 < fuzziness < 1:
        fuzziness = int(round(fuzziness * regex_len(pattern), 0))
    if fuzziness:
        pattern = '(' + pattern + '){e<=' + str(fuzziness) + '}'
    if r'{' in pattern or r'[' in pattern or '\\' in pattern:
        return regex.compile(pattern, **kwargs)
    if r'*' in pattern or r'#' in pattern:
        pattern.replace(r'*', r'[-a-zA-Z]+')
        pattern.replace(r'#', r'([-a-zA-Z]+[ ]{0,1})+')
        pattern.replace(r' ', r'[ ]')
        pattern.replace(r'[[ ]]', r'[ ]')
        return regex.compile(pattern, **kwargs)
    return pattern


class PatternMap:
    """ Like a dict, but with locality-sensitive hashes of keys, fuzzy regex keys, and redundant keys

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

    >>> patterns = PatternMap([('Hey', 'Hi!'), ('Hello *', 'Hey!')])
    >>> patterns['Hey']
    'Hi!'
    >>> patterns['Hello World!']
    'Hey!'
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
            pattern, template = pattern_template[0], pattern_template[1]
            pattern = compile_pattern(pattern)
            if isinstance(pattern, str):
                self.exact_strs[pattern] = self.exact_strs.get(pattern, []) + [template]
            else:
                self.patterns[pattern.pattern] = (
                    pattern, self.patterns.get(pattern.pattern, (pattern, []))[1] + [template])

    def __getitem__(self, statement):
        """ Returns a list of possible resonse templates based on a statement==pattern match """
        if statement in self.exact_strs:
            return self.exact_strs[statement]
        for (pattern_str, (pattern, templates)) in zip(self.patterns.keys(), self.patterns.values()):
            if pattern.match(statement):
                return templates
        return None

    def __str__(self):
        return str({'patterns': self.patterns, 'exact_strs': self.exact_strs})

    def __repr__(self):
        return self.__class__.__name__ + '<' + str({'patterns': self.patterns, 'exact_strs': self.exact_strs}) + '>'


class CallbackDict(dict):
    """ A dictionary that will attempt to call the callback in value before returning the bare value

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

    def __init__(self, on_say=print, response_mapping=None, context=None):
        self.response_mapping = response_mapping or RESPONSE_MAPPING
        self.on_say = on_say
        self.context = context or CONTEXT

    def say(self, s):
        self.on_say(s)
        return s

    def find_responses(self, statement):
        """ Generating the respond from the bot
        Args:
            args([int], [int]) : the probabilities of choosing choice A as the respond or choice B as the respond
        Returns:
            returns([str]) : The bot respond

        >>> respond('hi Bot',1,0)
        'Hi! How can I help you.'
        >>> respond('hi Bot',0,1)
        'Hi user, How can I help you?'
        """
        responses = []
        # O(N) algorithm must be improved with a pattern match search index or semantic search index like annoy
        for pattern, template in self.response_mapping:
            match = None
            try:
                match = pattern.match(statement)
            except AttributeError:
                if pattern == statement:
                    match = True
            if match:
                responses.append(template)
        return [r for (s, r) in self.response_mapping if s == statement]

    def respond(self, statement, min_confidence):
        """ Reply with the best response that meets the min confidence threshold """
        responses = self.find_responses(statement)
        resp = responses[0]
        self.say(resp)
