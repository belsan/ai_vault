## Info
flipbook.page is both a great example for AI agents and the full space of applying various models and techniques as well as a promising technique that we might use to enhance our product or to do fun projects with.

## How it works:
1) User defines any subject 
2) A diffusion model (flux 2) generates an informative image, with text and details. Like a drawing in a how things work book. This is displayed to the user
3) The user can then click on any part of the image
4) The frontend draws crosshairs around the point of the click, and sends it to a multimodal llm. "What is described here"
5) This becomes then the new prompt for the next iteration. So it is an endless zoom in these images.

## Notes:
a) There is a prompt generation llm, that takes the user subject, and probably the history of subjects, to create the flux prompt. That is important, as single-word ddescriptions would not work at all.
b) There is a streaming model used to create a video stream to seamlessly move between images
c) An agent in the background does a websearch to decide what information to show

## Why I like it as a basis for new projects & our product
It is hard to generate a UI completely via AI. Generating an image is easy, but how do you create feedback? Give the generator true freedom? The answer is surprisingly simple: draw where the user clicked and ask a multimodel llm to figure out the intent and move on. Truely a fully AI UI, no rulebased logic, no restrictions. Countless applications. Countless possibilities that were impossible a few months ago.

## Why I like it as a teaching example
It includes a bit of everything: 
* A diffusion model
* A simple llm to create prompts - nicely leading into prompt engineering, automatic prompt generation and quite a simple llm use.
* An agent loop - not visible at first, but in the background. Tool calls, web search, agent loop
* A streaming model
* A true use-case for a multimodal llm.
