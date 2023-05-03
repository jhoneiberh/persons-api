# python
from typing import Optional
from enum import Enum

# pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
from pydantic import HttpUrl

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
    city: str = Field(max_length=50)
    state: str = Field(max_lenght=50)
    country: str = Field(max_length=50)

    class Config:
        schema_extra = {
            'example': {
                'city': 'New York City',
                'state': 'New York',
                'country': 'EEUU'
            }
        }

class Person(BaseModel):
    first_name: str = Field(min_length=1, max_length=50, example='Facundo')
    last_name: str = Field(min_length=1, max_length=50, example='Garcia')
    age: int = Field(gt=0, le=115, example=21)
    hair_color: Optional[HairColor] = Field(default=None, example='black') # establecer un valo por defecto un parametro opcional
    is_married: Optional[bool] = Field(default=None, example=False)
    email: EmailStr = Field(example='correo@gmail.com')
    social_link: HttpUrl = Field(example='http://socialred.com/user')


    # class Config:
    #     schema_extra = {
    #         'example': {
    #             'first_name': 'Facundo',
    #             'last_name': 'Garcia',
    #             'age': 21,
    #             'hair_color': 'blonde',
    #             'is_married': False,
    #             'email': 'example@gmail.com'
    #         }
    #     }


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
                                description='This is the person name. It"s between 1 and 50 characters', 
                                example='Rocio'),
    age: str = Query(title='Person age', description='This is the person name. I"t required', example=21)
):
    return {
        name: age
    }


@app.get('/person/detail/{person_id}')
def show_person(
    person_id: int = Path(gt=0, example=15)

):
    return {person_id: 'It exists'}

# validaciones: request body

@app.put('/person/{person_id}')
def update_person(person_id: int = Path(title='Person ID', description='This is the person ID', gt=0, example=23), 
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