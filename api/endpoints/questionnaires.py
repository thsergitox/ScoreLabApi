from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import json

from db.models import Questionnaire
from db.session import SessionLocal
from openai_connection.models import ShortAnswer, MultipleChoice, TrueFalse

router = APIRouter()
db = SessionLocal()

shortAnswer = ShortAnswer()
multipleChoice = MultipleChoice()
trueFalse = TrueFalse()


class ModelRequest(BaseModel):
    kind: int
    theme: str
    subThemes: List[str]
    language: str
    content: str


class GetQuestionnaire(BaseModel):
    id: int

@router.post('/create')
async def root(req: ModelRequest):
    kind = req.kind
    theme = req.theme
    subthemes = req.subThemes
    language = req.language
    content = req.content

    if kind == 1:
        response = shortAnswer.generate_questions_json(theme, subthemes, content, language)['text'][0]['questions']
    elif kind == 2:
        response = multipleChoice.generate_questions_json(theme, subthemes, content, language)['text'][0]['questions']
    elif kind == 3:
        response = trueFalse.generate_questions_json(theme, subthemes, content, language)['text'][0]['questions']
    else:
        response = "Invalid type"

    new_questionnaire = Questionnaire(
        user_id=1,
        title=theme,
        description={"subthemes": subthemes, "content": content, "language": language, "kind": kind},
        questions={"questions": response}
    )
    db.add(new_questionnaire)
    db.commit()
    db.refresh(new_questionnaire)

    return {'res': response}


@router.get('/{id}')
async def get_questionnaire(id: int) -> dict:
    questionnaire = db.query(Questionnaire).filter(Questionnaire.id == id).first()
    if questionnaire:
        return {'title': questionnaire.title, 'description': questionnaire.description, 'questions': questionnaire.questions}
    else:
        return {'message': 'Questionnaire not found'}
