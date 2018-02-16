.. image:: https://travis-ci.com/aira/ai-chat.svg?token=bqTJyxXyR4BPUEzP78rW&branch=master
    :target: https://travis-ci.com/aira/ai-chat
====
Chat
====


This is a simple chatbot for testing natural language processing approaches. The chatbot architecture combines 3 approaches:

1. pattern matching (grammar-based appraoch)
2. search (retrieval-based approach)
3. grounding (knowledge-base approach)

You can build your own behaviors/skills by editing the data files in `src/aira/chat/data/*.csv` and then loading them into your chatbot's brain. The data folder contains example .csv files for riddles and other multi-turn dialog games.

Unlike other search and pattern-based chatbots, this architecture allows you to control context and build a decision tree of behaviors. You can hand-craft your behaviors or learn them from example dialog corpora.

Usage
===========

``` shell
$ hey Bot, "What's up?"
I heard you, but I'm not sure what you mean.
```
