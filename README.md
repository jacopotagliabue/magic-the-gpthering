# magic-the-gpthering
Playground for generating cards in the style of "Magic The Gathering" using generative AI


## Overview


The app is built as a Streamlit app, wrapping with Python the generative capabilities of OpenAI models, GPT and DALLE. The GPT prompts are built from some or less random cards (leveraging the database [here](https://scryfall.com/?utm_source=mci)).

## Generate cards

IMPORTANT: since we leverage OpenAI APIs, you need to have your own API key to generate cards. You can quickly sign up [here](https://openai.com/api/) to get one, if you don't have one already. The streamlit app doesn't store your credentials anywhere.

### Cloud app

## Running the code locally

The code was developed using Python 3.9. To run the app locally, clone the repo, setup a virtual environment and run the app from there:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_magic_app.py
```

A new browser window should open up, displaying the card generating app.

## What's next?

# License