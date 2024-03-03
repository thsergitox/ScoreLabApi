from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain

from config import settings

OPENAI_API_KEY = settings.OPENAI_API_KEY
NUM_OPTIONS = 3 # Define the number of options for multiple choice questions
MODEL = "gpt-3.5-turbo-0125"
TEMPERATURE = 0.5

class ShortAnswer:
    def __init__(self):
        self.schema = {
            "type": "object",
            "properties": {
                "questions_array": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "pregunta": {"type": "string"},
                            "respuesta": {"type": "string"},
                        },
                        "required": ["pregunta", "respuesta"],
                    },
                },
            },
            "required": ["questions_array"],
        }

        self.llm = ChatOpenAI(temperature=TEMPERATURE, model=MODEL, api_key=OPENAI_API_KEY)
        self.chain = create_extraction_chain(self.schema, self.llm)

    def generate_questions_json(self, theme, subthemes, content):
        # Format the subthemes and types for the prompt
        formatted_subthemes = ', '.join(subthemes)

        # Insert data into the template
        query = f"""Genera una lista de pares pregunta-respuesta en Español basados en el tema {theme}, cubriendo los subtemas {formatted_subthemes}. 
Aquí está el texto de contenido delimitado por comillas triples: 
\""" 
{content} 
\""" 
"""

        # Call the model with the formatted prompt
        response = self.chain.invoke(query)

        return response['text'][0]['questions_array']


class MultipleChoice:
    def __init__(self):
        self.schema = {
            "type": "object",
            "properties": {
                "questions_array": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "pregunta": {"type": "string"},
                            "opciones": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": NUM_OPTIONS,
                            },
                            "respuesta": {"type": "string"},  # Correct option
                        },
                        "required": ["pregunta", "opciones", "respuesta"],
                    },
                },
            },
            "required": ["questions_array"],
        }

        self.llm = ChatOpenAI(temperature=TEMPERATURE, model=MODEL, api_key=OPENAI_API_KEY)
        self.chain = create_extraction_chain(self.schema, self.llm)

    def generate_questions_json(self, theme, subthemes, content):
        # Format the subthemes and types for the prompt
        formatted_subthemes = ', '.join(subthemes)

        # Insert data into the template
        query = f"""Genera una lista de preguntas de opción múltiple en Español basadas en el tema {theme}, cubriendo los subtemas {formatted_subthemes}; incluye preguntas, opciones de respuestas e indica la respuesta correcta (solo una opción). 
Aquí está el texto de contenido delimitado por comillas triples: 
\""" 
{content} 
\""" 
"""

        # Call the model with the formatted prompt
        response = self.chain.invoke(query)

        return response['text'][0]['questions_array']

class TrueFalse:
    def __init__(self):
        self.schema = {
            "type": "object",
            "properties": {
                "questions_array": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "afirmación": {"type": "string"},
                            "truth_value": {"type": "boolean"},  # True or False
                        },
                        "required": ["afirmación", "truth_value"],
                    },
                },
            },
            "required": ["questions_array"],
        }

        self.llm = ChatOpenAI(temperature=TEMPERATURE, model=MODEL, api_key=OPENAI_API_KEY)
        self.chain = create_extraction_chain(self.schema, self.llm)

    def generate_questions_json(self, theme, subthemes, content):
        # Format the subthemes and types for the prompt
        formatted_subthemes = ', '.join(subthemes)

        # Insert data into the template
        query = f"""Genera una lista de 15 afirmaciones verdadero/falso en Español basadas en el tema {theme}, cubriendo los subtemas {formatted_subthemes}; incluye la afirmación y su valor de verdad (verdadero o falso).  
Aquí está el texto del contenido delimitado por comillas triples: 
\""" 
{content} 
\""" 
"""
        # Call the model with the formatted prompt
        response = self.chain.invoke(query)

        return response['text'][0]['questions_array']