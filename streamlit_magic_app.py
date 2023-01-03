import requests
import json
import time
import streamlit as st
from datetime import datetime
from prompts import GPT_PROMPT
from random import choice
from PIL import Image, ImageFont, ImageDraw
import textwrap


### Utility functions / API wrappers

# open AI vars
GPT_3_COMPLETION_URL = 'https://api.openai.com/v1/completions'
DALLE_URL = 'https://api.openai.com/v1/images/generations'

# initialize the card font
CARD_TITLE_FONT = ImageFont.truetype('24324_MAGIC.ttf', 24)
CARD_TEXT_FONT = ImageFont.truetype('Garamond Regular.ttf', 21)
CARD_FLAVOR_FONT = ImageFont.truetype('GARAIT.TTF', 21)
CARD_LEFT_MARGIN = 55

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


def write_paragraph_on_image(
    draw: ImageDraw,
    paragraph: str,
    y_text: int,
    font,
    char_width: int=42
):
    lines = textwrap.wrap(paragraph.strip(), width=char_width)
    for line in lines:
        width, height = font.getsize(line)
        draw.text((CARD_LEFT_MARGIN, y_text), line, (0,0,0), font=font)
        y_text += height
    # add margin between paragraphs
    y_text += (height * 0.6)

    return y_text


# generate the new card pic from the template
def draw_card(
        card_title: str,
        card_type: str,
        card_text: str,
        card_flavor: str,
        card_image: str
    ):
    # setup the card
    card_template = Image.open("card.jpeg")
    image_editable = ImageDraw.Draw(card_template)
    # title
    image_editable.text((CARD_LEFT_MARGIN, 45), card_title, (0,0,0), font=CARD_TITLE_FONT)
    # type
    image_editable.text((CARD_LEFT_MARGIN, 400), card_type, (0,0,0), font=CARD_TITLE_FONT)
    # now the main text: wrap lines when they are 40 char
    # first, break the text in paragraphs
    paragraphs = card_text.split('|')
    y_text = 450
    # limit to two
    for p in paragraphs[:2]:
        y_text = write_paragraph_on_image(
            image_editable,
            p,
            y_text,
            CARD_TEXT_FONT
        )
    # if card flavor, add it at the end
    if card_flavor:
        y_text = write_paragraph_on_image(
            image_editable,
            card_flavor,
            y_text,
            CARD_FLAVOR_FONT,
            char_width=48
        )
    # save the card
    card_template.save('new_card.jpg')

    return card_template


def get_value(
    field_name: str,
    features: list
):
    row = next((f for f in features if f.startswith(field_name)), '{}: n/a'.format(field_name))
    # get all the text after the first : separator
    content = ''.join(row.split(':')[1:]).strip()

    return content


def parse_gpt3_card_description(
    gpt_output: str
):
    # cut at the first card
    first_card = gpt_output.strip().split("===")[0].strip()
    # split on new line
    card_features = first_card.split('\n')
    print(card_features)
    _title = get_value('Card Name', card_features)
    _type = get_value('Types', card_features)
    _text = get_value('Card Text', card_features)
    _flavor = get_value('Flavor Text', card_features)
    # some post-processing
    _type = _type.replace('-', '')
    if _flavor == 'n/a':
        _flavor = None
    
    return _title, _type, _text, _flavor

# main function to generate new cards
def generate_new_card(
    api_key: str,
    card_color: str, 
    card_type: str
):
    # combine static prompt with color and type
    prompt = GPT_PROMPT.replace('my_color', card_color).replace('my_type', card_type)
    # get gpt 3 completion
    status_code, text = get_gpt3_completion(
        api_key=api_key,
        prompt=prompt,
        temperature=0.75,
        max_tokens=250
    )
    # if error, return the error and no card
    if status_code != 200:
        return "!!! Error when calling GPT (code {}): {}".format(status_code, text), None
    # parse gpt3 response into component
    _title, _type, _text, _flavor = parse_gpt3_card_description(text)
    # else, design the card
    card_template = draw_card(
        card_title=_title,
        card_type=_type,
        card_text=_text,
        card_flavor=_flavor,
        card_image=''
    )
    # debug
    print("Card generated at {}".format(datetime.utcnow()))
    # return the raw text and the image
    return text, card_template


### APP SECTION: Intro and credentials
st.header("Magic the GPThering - generating cards with AI")
st.write("This is a small app leveraging GPT-3 and DALLE-2 to generate magic cards in the style of the popular game. All code is open sourced: please consult the [GitHub project](https://github.com/jacopotagliabue/magic-the-gpthering) for more info.")
st.write("This was a fun week-end project and should be treated with the appropriate sense of humour: still lots of things to improve (check the repo if you want to contribute)!")

st.subheader("Credentials")
st.write("We need your OpenAI API to generate cards (attention: this will consume credits / add to your bill): sign up for one [here](https://openai.com/api/) if you don't have it!")
API_KEY = st.text_input("Enter your OpenAI API KEY", type="password")

### APP SECTION: Card generation
st.subheader("Card generation")    

color_options = ('White', 'Red', 'Blue', 'Black')
type_options = ('Creature', 'Sorcery', 'Enchantment', 'Instant')
color_option = st.selectbox('Pick a card color', color_options + ('Random',))
type_option = st.selectbox('Pick a card type', type_options + ('Random',))

# if user picked Random, select some random vals from the options
if color_option == 'Random':
    color_option = choice(color_options)

if type_option == 'Random':
    type_option = choice(type_options)

if st.button('Generate card'):
    card_text, card_image = generate_new_card(
        api_key=API_KEY,
        card_color=color_option,
        card_type=type_option
    )
    # display image
    if not card_image:
        st.write("Image could not be generated: check debug below for more info!")
    else:
        st.image(card_image, caption='My new card')
    # debug
    st.write('Raw text (debug')
    st.text(card_text)