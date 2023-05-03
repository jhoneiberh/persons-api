# python
from typing import Optional
from enum import Enum

# pydantic
from pydantic import BaseModel
from pydantic import Field

# fastapi
from fastapi import FastAPI
from fastapi import Body, Path, Query

app = FastAPI()

# Models


# lista de valores que se pueden usar
class HairColor(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    age: int = Field(gt=0, le=115)
    hair_color: Optional[HairColor] = Field(default=None) # establecer un valo por defecto un parametro opcional
    is_married: Optional[bool] = Field(default=None)

@app.get('/')
def home():
    return {
        'Hello': 'World'
    }


# request and response

@app.post('/person/new')
def create_person(person: Person = Body()):
    return person

# validaciones: query parameters

@app.get('/person/detail')
def show_person(
    name: Optional[str] = Query(None, min_length=1, max_length=50, title='Person Name', 
                                description='This is the person name. It"s between 1 and 50 characters'),
    age: str = Query(title='Person age', description='This is the person name. I"t required')
):
    return {
        name: age
    }


@app.get('/person/detail/{person_id}')
def show_person(
    person_id: int = Path(gt=0)

):
    return {person_id: 'It exists'}

# validaciones: request body

@app.put('/person/{person_id}')
def update_person(person_id: int = Path(title='Person ID', description='This is the person ID', gt=0), 
                person: Person = Body(),
                location: Location = Body()):
    
    # combinar 2 dicts en una sola variable
    # results = person.dict()
    # results.update(location.dict())
    # return results
    
    return {
        'person': person,
        'location': location
    }
    # results = {
    #     **person.dict(), **location.dict()
    # }
    
    # return {
    #     'person': person.dict(), 

    #     'location': location.dict()
    # }