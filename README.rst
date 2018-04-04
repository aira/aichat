.. image:: https://travis-ci.org/aira/aichat.svg?branch=master
    :target: https://travis-ci.org/aira/aichat
======
aichat
======


A chatbot framework for configuring and testing chatbot dialog specifications. 


Description
===========

`aichat` combines 2 approaches (more to come):

1. pattern matching (grammar-based appraoch)
2. search (retrieval-based approach)

Like AIML `aichat` allows you to control context and build a graph of behaviors (edges are chatbot actions/utterances). 
You can hand-craft your behaviors or "machine learn" them from example dialog corpora.

In the future `aichat` will incorporate a knowledge base (a grounding chatbot approach)

Usage
===========

``` shell
$ hey Bot, "What's up?"
I heard you, but I'm not sure what you mean.
```
