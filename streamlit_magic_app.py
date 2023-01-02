import requests
import json
import time
import streamlit as st
from datetime import datetime
from prompts import GPT_PROMPT


### Utility functions / API wrappers

# open AI vars
GPT_3_COMPLETION_URL = 'https://api.openai.com/v1/completions'
DALLE_URL = 'https://api.openai.com/v1/images/generations'

# wrap gpt3 API 
def get_gpt3_completion(
    api_key: str,
    prompt: str,
    temperature: float=0.5,
    max_tokens: int=0.5,
    model: str="text-davinci-002"
):
    start = time.time()
    data =  {
            "model": model,
            "prompt": prompt, 
            "temperature": temperature, 
            "max_tokens": max_tokens
            }
    payload = json.dumps(data)
    headers = { 
        'content-type': 'application/json', 
        "Authorization": "Bearer {}".format(api_key)
        }
    r = requests.post(GPT_3_COMPLETION_URL, data=payload, headers=headers)
    # print timing for debug
    print("GPT3 API time: {}".format(time.time() - start))
    # if the response is sound, get the first choice and return it
    gpt3_response = json.loads(r.text)["choices"][0]['text'].strip() if r.status_code == 200 else json.loads(r.text)['error']

    return r.status_code, gpt3_response

# main function to generate new cards
def generate_new_card(

):
    status_code, text = get_gpt3_completion(
        api_key=API_KEY,
        prompt=GPT_PROMPT,
        temperature=0.75,
        max_tokens=250
    )
    # debug
    print(text)
    # if error, return the error
    if status_code != 200:
        return "!!! Error when calling GPT (code {}): {}".format(status_code, text)
    # else, design the card

    # debug
    print("Card generated at {}".format(datetime.utcnow()))
    return text


### APP SECTION: Intro and credentials
st.header("Magic the GPThering - generating cards with AI")
st.write("This is a small app leveraging GPT-3 and DALLE-2 to generate magic cards in the style of the popular game. All code is open sourced: please consult the [GitHub project](https://github.com/jacopotagliabue/magic-the-gpthering) for more info.")

st.subheader("Credentials")
st.write("We need your OpenAI API to generate cards (attention: this will consume credits / add to your bill): sign up for one [here](https://openai.com/api/) if you don't have it!")
API_KEY = st.text_input("Enter your OpenAI API KEY", type="password")

### APP SECTION: Card generation
st.subheader("Card generation")    
if st.button('Generate card'):
    card_text = generate_new_card()
    # display the text
    st.write("Text debugging")
    st.text(card_text)

