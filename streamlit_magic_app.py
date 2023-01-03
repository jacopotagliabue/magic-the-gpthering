import requests
import json
import time
import streamlit as st
from datetime import datetime
from prompts import GPT_PROMPT
from random import choice
from PIL import Image, ImageFont, ImageDraw
import textwrap
from io import BytesIO


### Utility functions / API wrappers

# open AI vars
GPT_3_COMPLETION_URL = 'https://api.openai.com/v1/completions'
DALLE2_URL = 'https://api.openai.com/v1/images/generations'

# initialize the card font
CARD_TITLE_FONT = ImageFont.truetype('24324_MAGIC.ttf', 24)
CARD_TEXT_FONT = ImageFont.truetype('Garamond Regular.ttf', 21)
CARD_FLAVOR_FONT = ImageFont.truetype('GARAIT.TTF', 21)
CARD_LEFT_MARGIN = 55
IMG_WIDTH = 414
IMG_HEIGHT = 305
DALLE_SIZE = 512

# wrap dalle2 API
def get_dalle_image(
    api_key: str,
    prompt: str
):
    start = time.time()
    data =  {
          "prompt": prompt,
          "n": 1,
          "size": "512x512"
        }
    payload = json.dumps(data)
    headers = { 
        'content-type': 'application/json', 
        "Authorization": "Bearer {}".format(api_key)
        }
    r = requests.post(DALLE2_URL, data=payload, headers=headers)
    # print timing for debug
    print("DALLE3 API time: {}".format(time.time() - start))
    # if the response is sound, get the first choice and return it
    dalle_response = json.loads(r.text)["data"][0]['url'] if r.status_code == 200 else json.loads(r.text)['error']

    return r.status_code, dalle_response

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


def generate_dalle2_prompt(
    card_name: str,
    card_type: str,
    card_color: str
):  
    dalle_2_prompt_template = """
    A digital illustration of a {name} in the forefront in the middle. Background with {color} tones and {element} color schemes. 8k, detailed mythical {_type}, fantasy vivid colors in the style of Magic cards. Gorgeous digital painting, amazing art, artstation 3, realistic.
    """
    color_2_element = {
        'Blue': 'ocean and water', 
        'White': 'prairie and marble', 
        'Red': 'fire and cave', 
        'Black': 'swamp and dark',
        'Green': 'forest and wood'
    }    

    values = {
        'name': card_name,
        'color': card_color.lower(),
        'element': color_2_element[card_color],
        '_type': 'creature' if 'Creature' in card_type else card_type.lower()
    }

    return dalle_2_prompt_template.format(**values).strip()


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
    response = requests.get(card_image)
    card_image = Image.open(BytesIO(response.content))
    # resize and crop
    newsize = (IMG_WIDTH, IMG_WIDTH)
    v_margin = (DALLE_SIZE - IMG_HEIGHT) / 2
    small_card_image = card_image.resize(newsize)
    cropped_card_image = small_card_image.crop((0, v_margin, IMG_WIDTH, DALLE_SIZE - v_margin))
    card_template.paste(cropped_card_image, (43, 82))
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
    # generate image
    #image_text = 'https://oaidalleapiprodscus.blob.core.windows.net/private/org-l6VUPYjZmnBAEEzxRqH3HEz6/user-j5mZ9QYUln92c3nhg3nHfgMV/img-d3cM6zj7WZ8W2AnCo9Ybjd0H.png?st=2023-01-03T17%3A11%3A20Z&se=2023-01-03T19%3A11%3A20Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-01-03T16%3A12%3A40Z&ske=2023-01-04T16%3A12%3A40Z&sks=b&skv=2021-08-06&sig=6VXnC3j8iwIXBvoYF5IESrM73KEEZo%2BB6LvdMZgXA/Y%3D' 
    dalle2_prompt = generate_dalle2_prompt(_title, _type, card_color)
    status_code, image_text = get_dalle_image(
        api_key=api_key,
        prompt=dalle2_prompt
        )
    if status_code != 200:
        return "!!! Error when calling DALLE (code {}): {}".format(status_code, image_text), None
    # if all good, design the card
    card_template = draw_card(
        card_title=_title,
        card_type=_type,
        card_text=_text,
        card_flavor=_flavor,
        card_image=image_text
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

color_options = ('Blue', 'White', 'Red', 'Black', 'Green')
type_options = ('Creature', 'Enchantment', 'Artifact')
color_option = st.selectbox('Pick a card color', color_options + ('Random',))
type_option = st.selectbox('Pick a card type', type_options + ('Random',))

# if user picked Random, select some random vals from the options
if color_option == 'Random':
    color_option = choice(color_options)

if type_option == 'Random':
    type_option = choice(type_options)


st.write('NOTE: card generation involves several API calls, give it 10 seconds or so!')
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
    st.write('Raw text (debugging purposes)')
    st.text(card_text)