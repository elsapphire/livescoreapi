import requests
# from openai import OpenAI
# import pathlib
import textwrap
import os

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


def to_markdown(txt):
    txt = txt.replace('•', '  *')
    return Markdown(textwrap.indent(txt, '> ', predicate=lambda _: True))


match_commentary_link = os.environ['MATCH_COMMENTARY']
sheety_api_link = os.environ['SHEETY_API']
gpt_api_key = os.environ['GPT_API']

gemini_api_key = os.environ['GEMINI_API']
genai.configure(api_key=gemini_api_key)


params = {
    'match_id': 335680,
    'key': 'pg65SXZVXohsQrOQ',
    'secret': os.environ['SECRET']
}
response = requests.get(match_commentary_link, params=params)
result = response.json()
data = result['data']['commentary']
event_type = data[0]['event_type']
minute = data[0]['minute']
second = data[0]['second']
comment = data[0]['comment']
text = data[0]['text']


# {'id': 413, 'match_id': 334919, 'event_type': 'DRAW', 'minute': 'FT', 'second': 'FT', 'match_second': 253331,
# 'comment': '', 'pos_x': 0, 'pos_y': 0, 'side': '', 'created_at': '2022-06-09 17:09:43', 'updated_at': None,
# 'text': 'The match ends in a draw', 'team': [], 'player': [], 'player_2': []}
model = genai.GenerativeModel('gemini-pro')
# response = model.generate_content(f"Generate a question and and answer from this text Croatia is the match winner")
# question = response.text
# first_split = question.split(':')
# print(first_split)
# q = first_split[1].strip('** \n\n**Answer')
# a = first_split[2].strip('** ')

print(data[0])
for r in data:
    response = model.generate_content(f"Generate a question and and answer from this text {r['text']}")
    question = response.text
    first_split = question.split(':')

    print(r)
    my_dict = {
        "sheet1": {
            'question': first_split[1].strip('** \n\n**Answer'),
            'answer': first_split[2].strip('** ')
        }
    }
    print(my_dict)
    sheet = requests.post(sheety_api_link, json=my_dict)
    print(sheet.text)
# print(response.prompt_feedback)


# to_markdown(response.text)

# client = OpenAI(api_key=gpt_api_key)
# completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts
#         with creative flair."},
#         {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
#       ]
# )
#
# print(completion.choices[0].message)
