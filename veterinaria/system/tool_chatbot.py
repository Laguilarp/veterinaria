import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

# Used to securely store your API key

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


genai.configure(api_key='AIzaSyAHnSTThuUwnLOviBNAptDYvv_N6HhAor4')
model = genai.GenerativeModel('gemini-1.5-flash')

def consulta(mensaje):
    response = model.generate_content(mensaje)
    return to_markdown(response.text).data