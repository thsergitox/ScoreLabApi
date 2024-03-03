from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session
from fastapi import Depends

from db.models import Questionnaire
from db.session import SessionLocal
from openai_connection.models import ShortAnswer, MultipleChoice, TrueFalse

router = APIRouter()


shortAnswer = ShortAnswer()
multipleChoice = MultipleChoice()
trueFalse = TrueFalse()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ModelRequest(BaseModel):
    kind: int
    theme: str
    subThemes: List[str]
    content: str


@router.post('/create')
async def root(req: ModelRequest,  db: Session = Depends(get_db)):
    kind = req.kind
    theme = req.theme
    subthemes = req.subThemes
    content = req.content

    if kind == 1:
        response = shortAnswer.generate_questions_json(theme, subthemes, content)
    elif kind == 2:
        response = multipleChoice.generate_questions_json(theme, subthemes, content)
    elif kind == 3:
        response = trueFalse.generate_questions_json(theme, subthemes, content)
    else:
        response = "Invalid type"

    try:

        new_questionnaire = Questionnaire(
            user_id=1,
            title=theme,
            description={"subthemes": subthemes, "content": content, "kind": kind},
            questions={"questions": response}
        )
        db.add(new_questionnaire)
        db.commit()
        db.refresh(new_questionnaire)

        return {'res': response, "id": new_questionnaire.id}
    except DatabaseError:
        return {'res': 'User does not exist or bad query'}


@router.get('/{id}')
async def get_questionnaire(id: int, db: Session = Depends(get_db)) -> dict:
    questionnaire = db.query(Questionnaire).filter(Questionnaire.id == id).first()
    if questionnaire:
        return {'title': questionnaire.title, 'description': questionnaire.description, 'questions': questionnaire.questions}
    else:
        return {'message': 'Questionnaire not found'}
