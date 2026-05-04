Feedback: 30 April, version 0.1


## front matter: 

* add the PhD to my name, add Chipmind AG as my company and add something like "assistance: Claude Opus 4.7" to indicate that I had help from you.
* Add a version number. 


## tool calls:

In general I'm am struggeling a bit with how to define toolcalls - is a toolcall in a single llm interaction even meaningful? Usually you need query, reply with toolcall, and observation back to the llm for the final answer. But that is already almost an agent loop, which I would like to treat separately. 
Right now it suddenly shows up in the generic implementation "The LOOP" - absolutely central and introduced matter-of-factly.

### The strawberry problem
add a note that the problem has been partially addressed. GPT version 5.4 seems to get it correct but there are reports that it still trips up if spelling mistakes are added (how many ps are in strawpberry) or even already at cranberry. 
I have also added a picture of Opus 4.7 getting the misspelled strawpberry wrong. Add the picture and also have a note with the release date of opus 4.7. The picture is a webp in this feedback folder, you will need to move it somewhere more appropriate.

### After "What is a Tool Call"
After what is a tool call there should be a practical example with the letter count thing. A description of an exchange. Along those lines
1) query to the llm contains extra information about the tools it can call. Describe what we send, the count_letters tool with its arguments
2) The llm decides if and what tool to call
3) In this case it decides to call the word count, show what its answer looks like
4) The response has to be parsed, the tool call extracted, and executed.
5) The tool call output has to be captured and sent back to the llm
6) The llm replies with the final answer

With that, we can then create a list of things we need to implement in the generic implementation.

I have seen people confused about what happens where, and confused about the description we send to the llm versus the actual implementation that runs the tool.

### Generic implementation
Here I want some llm agnostic description of the main building blocks as mentioned above. We need a description of the tools for the llm, a function which runs the tool, logic to parse the response into toolcalls and the main loop. This scaffolding, which can be pseudocode, can then guide us through the actual implementations. This then also changes the openai implementation, as the concepts should be clear. Side note: clean the code up slightly, with a function and a name==__main__ that calls the query function with the question.

### The gemma4 case
This is a bit tricky: gemma4 does natively support tool calls, but the return format is different. Because I want to use gemma4 throughout the book, we have to deal with that. Check the actual syntax and create a script to run, to make sure it is correct.

### No native support
This does not need a fully working example. But a discussion: how do we get a model to output toolcalls? We have to give instructions and examples. Give part of the system prompt to show. To do this properly, we need to add a new chapter. Something like LLM fundamentals. In there we should have a section about structured outputs. How to get the model to do that, applications, etc. 


### Taxonomy of common toolcalls
Should have a subchapter with practical examples. Also, mention websearch as a powerful tool somewhere.

### Shell as a tool
Add a second example where a file is written and executed (python script)

### Risks
Sandboxing does not only help with critical "delete everything" problems, but also with the agent messing with the system. It will happily install programs, change versions of existing tools, install python packages, etc. A sandbox makes this a non-issue.
The second recommendation to add is version control. If the agent runs on version controlled files, there is another layer of security. Of course, technically it can still rewrite the history, depending on the setup, but still a good best practice. 









