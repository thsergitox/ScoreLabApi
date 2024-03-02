from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain

from config import settings

OPENAI_API_KEY = settings.OPENAI_API_KEY
NUM_OPTIONS = 3 # Define the number of options for multiple choice questions
MODEL = "gpt-3.5-turbo"


class ShortAnswer:
    def __init__(self):
        self.schema = {
            "type": "object",
            "properties": {
                "questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "answer": {"type": "string"},
                        },
                        "required": ["question", "answer"],
                    },
                },
            },
            "required": ["questions"],
        }


        self.llm = ChatOpenAI(temperature=0, model=MODEL, api_key=OPENAI_API_KEY)
        self.chain = create_extraction_chain(self.schema, self.llm)

    def generate_questions_json(self, theme, subthemes, content, language):
        # Format the subthemes and types for the prompt
        formatted_subthemes = ', '.join(subthemes)

        # Insert data into the template
        query = f"""Generate a list of question-answer pairs based on the theme {theme}, generate  covering the subthemes {formatted_subthemes}; in the language {language}. Here is the content: {content} """

        # Call the model with the formatted prompt
        response = self.chain.invoke(query)

        return response


class MultipleChoice:
    def __init__(self):
        self.schema = {
            "type": "object",
            "properties": {
                "questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "options": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": NUM_OPTIONS,
                            },
                            "answer": {"type": "string"},  # Correct option
                        },
                        "required": ["question", "options", "answer"],
                    },
                },
            },
            "required": ["questions"],
        }

        self.llm = ChatOpenAI(temperature=0, model=MODEL, api_key=OPENAI_API_KEY)
        self.chain = create_extraction_chain(self.schema, self.llm)

    def generate_questions_json(self, theme, subthemes, content, language):
        # Format the subthemes and types for the prompt
        formatted_subthemes = ', '.join(subthemes)

        # Insert data into the template
        query = f"""Generate a list of multiple-choice questions based on the theme {theme}, covering the subthemes {formatted_subthemes}; include questions, options for answers, and indicate the correct answer, in {language}. Here is the content: {content}"""

        # Call the model with the formatted prompt
        response = self.chain.invoke(query)

        return response

class TrueFalse:
    def __init__(self):
        self.schema = {
            "type": "object",
            "properties": {
                "questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "statement": {"type": "string"},
                            "truth_value": {"type": "boolean"},  # True or False
                        },
                        "required": ["statement", "truth_value"],
                    },
                },
            },
            "required": ["questions"],
        }

        self.llm = ChatOpenAI(temperature=0, model=MODEL, api_key=OPENAI_API_KEY)
        self.chain = create_extraction_chain(self.schema, self.llm)

    def generate_questions_json(self, theme, subthemes, content, language):
        # Format the subthemes and types for the prompt
        formatted_subthemes = ', '.join(subthemes)

        # Insert data into the template
        query = f"""Generate a list of true/false statements based on the theme {theme}, covering the subthemes {formatted_subthemes}; include the statement and its truth value (true or false), in {language}. Here is the content: {content}"""

        # Call the model with the formatted prompt
        response = self.chain.invoke(query)

        return response
