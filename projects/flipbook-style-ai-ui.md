# Flipbook-style AI UI

**Status:** parked idea
**Origin:** inspired by [flipbook.page](https://flipbook.page)
**Tags:** UI, multimodal, agents, teaching example

---

## Pitch

`flipbook.page` is the cleanest existing demonstration of a fully AI-generated UI:

1. The user picks any subject.
2. A diffusion model (Flux 2) generates an *informative* image — text, callouts, the look of a "how things work" book illustration.
3. The user clicks anywhere on the image.
4. The frontend draws crosshairs at the click point and asks a multimodal LLM, "what is described here?"
5. That answer becomes the new prompt for the next image — endless zoom, endless drill-down.

The trick that makes it work: there is no rule-based UI logic. The "interaction" is just *draw a marker where the user pointed and let a multimodal LLM read intent*.

## Why I like it as a basis for new projects (and our product)

It's normally hard to build a UI fully via AI. Generating an image is easy; getting structured feedback from the user without falling back to forms/buttons is the hard part. Flipbook's answer — draw the click and ask a multimodal LLM — is surprisingly simple and unlocks a lot of designs we would otherwise consider impossible.

For our product specifically, the "click on a part of the rendered diagram, get a contextual response" pattern is directly applicable to RTL schematic / waveform / coverage exploration.

## Why I like it as a teaching example

The system contains a bit of *everything* a working agent product has, in a small enough footprint to fit in one lecture:

- **Diffusion model** — the image generator.
- **Prompt-construction LLM** — turns the user's subject and history of subjects into a useful Flux prompt. Natural lead-in to prompt engineering and automatic prompt generation.
- **Agent loop in the background** — web-searches in the background to decide what information the next illustration should foreground. Tool calls, search, loop.
- **Streaming model** — produces the seamless video transitions between illustrations.
- **Multimodal LLM** — reads the click + image and decides what the user meant. This is the part that turns the image into a UI.

## Open questions / next steps

- What fraction of the user's "click intent" can a multimodal LLM actually reconstruct robustly? Worth a small pilot.
- Could the same pattern be driven by a *schematic* renderer instead of a diffusion model — i.e. real RTL diagram + click + multimodal interpretation? That's the version that's directly relevant to our product.
- Lecture-form storyboard: 6 sections, one per component above. Would slot well as a single chapter in the manuscript.

## See also

- The `agents/` folder for the harness papers (CodeAct, ACE).
- The `models-and-training/` folder for the SLM-based small-model arguments — relevant if we want this teaching demo to run on modest hardware.
