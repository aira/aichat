#!/usr/bin/env python
# -*- coding: utf-8 -*-
from aichat import constants
from aichat import brain
from aichat import context
from aichat import pattern
from aichat import audio

import doctest


__author__ = "Aira"
__copyright__ = "Aira"
__license__ = "mit"


# def test_respond():
#     assert brain.respond('hi') in (
#         r"Hi! I'm Bot. How can I help you?",
#         r"Hi! I'm Bot. I'm here to assist you. I can describe a scene by recognizing objects."
#         )

def test_constants():
    assert doctest.testmod(constants, raise_on_error=True)


def test_brain():
    assert doctest.testmod(brain, raise_on_error=True)


def test_context():
    assert doctest.testmod(context, raise_on_error=True)


def test_pattern():
    assert doctest.testmod(pattern, raise_on_error=True)


def test_audio():
    assert doctest.testmod(audio, raise_on_error=True)

