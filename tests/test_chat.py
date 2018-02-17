#!/usr/bin/env python
# -*- coding: utf-8 -*-
from aichat.chat import respond


__author__ = "Aira"
__copyright__ = "Aira"
__license__ = "mit"


def test_respond():
    assert respond('hi') in (
        r"Hi! I'm Bot. How can I help you?",
        r"Hi! I'm Bot. I'm here to assist you. I can describe a scene by recognizing objects."
        )
