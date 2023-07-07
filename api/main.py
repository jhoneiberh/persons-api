"""FastAPI."""
# python
from typing import Optional
from enum import Enum
import uvicorn

# pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
from pydantic import HttpUrl

# fastapi
from fastapi import FastAPI
from fastapi import status
from fastapi import Body
from fastapi import Path
from fastapi import UploadFile
from fastapi import File
from fastapi import Query
from fastapi import Form
from fastapi import Header
from fastapi import Cookie
from fastapi import HTTPException

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


@app.get('/', status_code=status.HTTP_200_OK, tags=['Home'])
def home():
    """
    Home.

    This path operation gives a World message

    Parameters: 
    - Nothing

    Returns: World
    """
    return {
        'Hello': 'World'
    }


# request and response

@app.post('/person/new', status_code=status.HTTP_201_CREATED ,response_model=PersonOut, tags=['Persons'], 
        summary='Create Person in the app')
def create_person(person: Person = Body()):
    """
    Create Person.

    This path operations creates a person in the app and save the information in the database

    Parameters: 
    - Request body parameter
        - **person: Person** -> A person model with first name, last name, age, hair color, marital status and password.
    
    Returns: A person model with first name, last name, age, hair color and marital status.
    """
    return person

# validaciones: query parameters

@app.get('/person/detail', status_code=status.HTTP_200_OK, tags=['Persons'], deprecated=True)
def show_person(
    name: Optional[str] = Query(None, min_length=1, max_length=50, title='Person Name', 
                                description='This is the person name. It"s between 1 and 50 characters', 
                                example='Rocio'),
    age: str = Query(title='Person age', description='This is the person name. I"t required', example=21)
):
    """
    Show Person.

    This path operation displays the information of a user that is sent by query parameters

    Parameters: 
    - Query parameters: 
        - name and age

    Returns: The name and age of the user
    """
    return {
        name: age
    }

# Validaciones: Path parameters

persons = [1, 2, 3, 4, 5]

@app.get('/person/detail/{person_id}', status_code=status.HTTP_200_OK, tags=['Persons'])
def show_person(
    person_id: int = Path(gt=0, example=15)

):
    """
    Show Person.

    This path operations show if an user exists in the database

    Parameters: 
    - Id of the user

    Returns: A message saying if user exists in the database.
    """
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='¡This person doesn\'t exist!'
        )
    
    return {person_id: 'It exists'}

# validaciones: request body

@app.put('/person/{person_id}', status_code=status.HTTP_201_CREATED, tags=['Persons'])
def update_person(person_id: int = Path(title='Person ID', description='This is the person ID', gt=0, example=23), 
                person: Person = Body(),
                location: Location = Body()):
    
    # combinar 2 dicts en una sola variable
    # results = person.dict()
    # results.update(location.dict())
    # return results
    """
    Update Person.

    This path operation update user information

    Parameters: 
    - ID of the user
    - Request Body: 
        - **person: Person** -> A person model with first name, last name, age, hair color, marital status and password.
        - **location: Location** -> A location model with city, state and country.

    Returns: A person model with first name, last name, age, hair color and marital status; and the 
    information about location of the user
    """    
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

# Forms

@app.post('/login', response_model=LoginOut, status_code=status.HTTP_200_OK, tags=['Persons'])
def login(username: str = Form(), password: str = Form()):
    """
    Login.

    This path parameters allows the user login in the website

    Parameters: 
    - Form:
        - username and password

    Returns: The username and a message saying login succesfuly!
    """    
    # login = LoginOut(username=username)
    # return login

    return LoginOut(username=username)

# Cookies and Headers Parameters

@app.post('/contact', status_code=status.HTTP_200_OK, tags=['Contact'])
def contact(first_name: str = Form(max_length=20, min_length=1), 
            last_name: str = Form(max_length=20, min_length=1),
            email: EmailStr = Form(),
            message: str = Form(min_length=20), 
            user_agent: Optional[str] = Header(default=None),
            ads: Optional[str] = Cookie(default=None)):
    """
    Contact.

    This path paramater allows send a message.

    Parameters:
    - Form:
        - first name, last name, email, message, user agent and ads

    Retuns: user agent of the user
    """
    return user_agent


# Files

@app.post('/post-image', tags=['Files'])
def post_image(image: UploadFile = File()):
    """
    Post Image.

    This path parameter allows upload a image.

    Parameters:
    - File:
        - Any file likes image, documents

    Returns: Filename, formant file and size in KiloBytes.
    """
    return {
        'Filename': image.filename,
        'Format': image.content_type,
        # 'Size(kB)': round( len(image.file.read()) / 1000, ndigits=1)
        'Size(kB)': round(image.size / 1000, ndigits=1)
    }

if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)