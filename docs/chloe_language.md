# Chloe Language

Let's put AIML to bed once and for all and talk about a new way of specifying chatbots. Having an AIML interpreter on the Android device is a very important feature, for mimicing complex behaviors of other open source AIML bots. But I think there's a better way for us to specify **new** Chloe behaviors. It's not a new approach, it's used for most commercial chatbots, but it's more commonly used for web applications for GET response programming... you'll see that when I show examples.

There's a way to specify Chloe behavior in a language (actually 2 languages) that is as powerful as AIML but much easier to program, and maintain (and to program/maintain/extend an interpreter for). So easy, in fact, that I think by the end of the year we could make it possible for Explorers like Greg to "develop" very complex Chloe behaviors. And I think that together we can design such a language. I don't know what the implementation looks like, except for a few simple example behaviors (below).

Once we settle on this general approach, we can bring in others like Greg and Juan to get their feedback on the language and how best to incrementally improve/simplify it.

## We need 2 languages:

1. A way to specify a trigger/command (the `if` conditional) and another for specifying Chloe actions (responses). At it's most basic level, the trigger language could be a lot like "glob *" patterns like AIML 1.0 triggers, or URL regex patterns in Django and Flask. An interpreter for such a language is almost trivial and there are several python and java libraries that can interpret glob * patterns.

2. A way to specify Chloe's action/response. Since we are specifying a string to be said, a starting poing could be jinja2 or even the builtin `.format()`python string interpolation language. Any language that specifies string templates populated with a dictionary/mapping of key-value pairs. In python, the dictionary could be the output of `locals()` to provide all the data available within the namespace of the interpreter, or it could be a huge `kwargs` dictionary containing the "context" of the current conversation, just like in Django and Flask. I don't know of any Android template interpreters, but all modern programming languages have a string interpolation language built in. I'm sure there are equivalents to jinja2.

## Examples

The simplest example of this 2-language (2-column csv) language might be:

    "Hi Chloe", "Hi! How can I help you."

A slightly more complex one might be:

    "Hi Chloe", "Hi {user.first_name}, How can I help you?"


OR

    "Hey|Hi Chloe|Klo, what time is it", "Hi {user.first_name}, it's {now.hour} {now.minute:02d}."

And for the "read" command it might be:

    "* Chloe * read *", "Hi {user.first_name}, here's what I see at the moment. Tell me when to stop. {ocr.text}"

If we're doing things right, text should be ready for us on the Android phone before this command is even finished from the user. The variable `ocr.text` would have been populated with the latest image with the most text in it (some balance of the 2 in our objective function).

One final example from the UX meeting:

    "Help", "Hi {user.first_name}, here's the sort of things I can do {docs.commands[:5].join(',')}. Would you like to learn more?

## Help!!

There are devils in the details, like:

1. the appropriate "fuzziness" of our pattern recognizer, and a way to specify it in the language
2. the simplest way to specify complex data queries
3. how to specify a dialog "chain" or "tree"
4. how to specify more complex actions involving nested conditionals
5. how to specify a language that specifies trigger based on non-verbal information (e.g. reminders at a particular time of day each way, I have an idea for this that would work with our glob * interpreter).
6. ways to compute "confidence" in the intent recognizer

## Nonverbal Triggers

If we specify the triggers as key-value pairs, with a key that specifies the source of the "statement" (string), we can handle a lot of simple nonverbal triggers.  
We could even specify the keys just like RMQ topics with slashes, hashes, and stars, so that they could refer to remote data sources.

    "now/first_exceedance/2018/01/26/12/00": "It's time for that weekly AI brownbag!" 
or

    "now/first_exceedance/Mon/12/00": "It's time for that weekly AI brownbag!" 

verbal triggers might be specified like

    "user/1234": "It's time for that weekly AI brownbag!" 

Alternatively those keys could also be specified in natural language and be passed through our pattern matcher too to generate RMQ path patterns automatically. 

## Plan


1. python interpreter of chloe language CSV (string->string matching)
2. 
- add globstar
- add string interpolation (jinja2 or .format())
- hook it up to slack
- hook it up to TTS and STT

