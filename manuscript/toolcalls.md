# Toolcalls

(Unsure how to order and structure all of this)

## Motivating simple example
Even highly trained, top-of-the-line llms can't count letters. Screenshots of people asking "how many r are in straberry" and it failing and on newer versions like gpt 5.4, they ask "how many ps in straperry". LLMs are not good at counting. That is a fundamental limitation. However, classic software is great at that - writing a python function that returns the number of a certain character in a word sounds like a task for an early "intro to programming" course. 
Toolcalls can bridge this gap - let the llm do what it is good at and if it encounters something it needs help with, let it call a tool. 

In fact, this extremely though problem that the most advanced llms struggle with, counting letters, can easily be implemented as a tool call.

(philosophically, it is my belief that toolcalls are overcoming fundamental limits of llms and therefore augment the capability of any llm system fundamentally)


## What are toolcalls
General description and example of a transaction of a letter count example.

## Generic implementation
A hands-on python example that fully implements a simple toolcall functionality. Two flavours: hyperscalar, e.g. openai, where toolcalls are nicely handled for you. Then a gemma4 example, where a little extra work is needed

## Toolcalls if the model does not support them natively
An example for a model where we have to do all the heavy lifting ourselves. Give examples and get it to produce nice json output.

## Typical tool calls
Toolcalls not only address limitations, but also allow interaction with the real world. From reading the time, to getting weather information, to ... (add examples)


## The powerhouse: shell commands
People might underestimate how powerful an agent with a shell toolcall, e.g. a bash toolcall is. That allows retrieval with grep and find, reading and writing (!) files, executing python code, testing generated code in the environment, and interacting with the environment, the running processes, the env variables. It can even install programs. It can interact with git, the web through curl, the possibilities are endless. (give concrete examples of shell commands)


Then a few notes on the dangers and also a recommendation to sandbox, e.g. in docker.

## The underrated superpower: writing and executing code
LLMs exceed at writing code. If it can write and execute python code that opens a whole new level of capabilies. Anthropic also suggests what it calls programmatic toolcalling. 

## Outlook: Toolcalls as the gateway to agents
Essentially, the "toolcalls elicit better llm agents" paper can make a nice transition into an agents chapter.
