# magic-the-gpthering
Playground for generating cards in the style of "Magic The Gathering" using generative AI


## Overview


The app is built as a Streamlit app, wrapping with Python the generative capabilities of OpenAI models, GPT and DALLE. The GPT prompts are built from some or less random cards (leveraging the database [here](https://scryfall.com/?utm_source=mci)).

## Generate cards

IMPORTANT: since we leverage OpenAI APIs, you need to have your own API key to generate cards. You can quickly sign up [here](https://openai.com/api/) to get one, if you don't have one already. The streamlit app doesn't store your credentials anywhere.

### Cloud app

Browse to our Streamlit app here - you should be able to generate cards directly on your browser (if the app is "sleeping" on the Streamlist servers, follow the browser instructions to spin it up again).

### Running the code locally

The code was developed using Python 3.9. To run the app locally, clone the repo, setup a virtual environment and run the app from there:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_magic_app.py
```

A new browser window should open up, displaying the card generating app.

## What's next?

Of course, everything feels a bit hacky, as it should be for a fun week-end project! There are milion ways you could try and improve all of this, for example:

* improving the card generation process with some more details on the card (for example, font / better rendering of small elements, check for text size etc.), as well as supporting multiple card templates (green, white, lands etc.);
* better prompting for GPT3;
* using other generative AI systems for the image (Midjourney has a fantasy touch, but no API still!);
* generate multiple images for the same card and let the user pick one.

Feel free to star this repo, fork the code and build your own generator!

## License

All the code is released without warranty, "as is" under a MIT License. We are not affiliated with, endorsed, sponsored, enchanted, truth or dare, by Wizards of the Coast LLC, OpenAI etc. This was a fun week-end project and should be treated with the appropriate sense of humour.

We are indeed very grateful to Wizards of the Coast for the endless amount of fun we had as kid: "When we was young, oh man, did we have fun / Always, always".