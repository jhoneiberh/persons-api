
# lista de valores que se pueden usar
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, HttpUrl


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

class PersonBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=50, example='Facundo')
    last_name: str = Field(min_length=1, max_length=50, example='Garcia')
    age: int = Field(gt=0, le=115, example=21)
    hair_color: Optional[HairColor] = Field(default=None, example='black') # establecer un valo por defecto un parametro opcional
    is_married: Optional[bool] = Field(default=None, example=False)
    email: EmailStr = Field(example='correo@gmail.com')
    social_link: HttpUrl = Field(example='http://socialred.com/user')

class Person(PersonBase):
    password: str = Field(min_length=8, example='hmjscdewfj')


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

class PersonOut(PersonBase):
    ... # es lo mismo que pass

class LoginOut(BaseModel):
    username: str = Field(max_length=20, example='Miguel06')
    message: str = Field(default='Login Succesfuly!')