This chapter has the information that is needed to get through the rest of the book.
# Context
What is it? What is in it?

# Structured outputs
Naively, an llm produces text. However, for a lot of applications json output, a query language, a function signature, or similar is the better choice. 
# Prompting

## Notes on Reproducability
Hyperscalars hide their llms, and phase out old ones. Results with their APIs can rarely be reproduced a year later. Explain the recent drama around anthropic reducing the thinknig time (which, according to them, was just a change in claude code), and also mention the phase-out of popular models.
In this manuscript we will use gemma4 for our experiments. For exactly that reason.

## Prompting Advice
All advice here should be: a) quoted and b) confirmed with a simple gemma4 prompt experiment.

## Oddities
Unclear how to call this section. But essentially: a lot of weird things happen and it is hard to pinpoint good advice. The capitalization is all you need paper, the paper that tells us that prompt duplication helps. 

## Context > Prompt
Some notes on the fact that constructing a good context is the actual, important goal.
