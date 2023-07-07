from typing import Optional
from fastapi import APIRouter, Body, Cookie, File, Form, Header, Query, UploadFile, status, Path, HTTPException
from pydantic import EmailStr

from api.models import Person, PersonOut, Location, LoginOut

router = APIRouter()

@router.get('/', status_code=status.HTTP_200_OK, tags=['Home'])
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

@router.post('/person/new', status_code=status.HTTP_201_CREATED ,response_model=PersonOut, tags=['Persons'], 
        summary='Create Person in the router')
def create_person(person: Person = Body()):
    """
    Create Person.

    This path operations creates a person in the router and save the information in the database

    Parameters: 
    - Request body parameter
        - **person: Person** -> A person model with first name, last name, age, hair color, marital status and password.
    
    Returns: A person model with first name, last name, age, hair color and marital status.
    """
    return person

# validaciones: query parameters

@router.get('/person/detail', status_code=status.HTTP_200_OK, tags=['Persons'], deprecated=True)
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

@router.get('/person/detail/{person_id}', status_code=status.HTTP_200_OK, tags=['Persons'])
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

@router.put('/person/{person_id}', status_code=status.HTTP_201_CREATED, tags=['Persons'])
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

@router.post('/login', response_model=LoginOut, status_code=status.HTTP_200_OK, tags=['Persons'])
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

@router.post('/contact', status_code=status.HTTP_200_OK, tags=['Contact'])
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

@router.post('/post-image', tags=['Files'])
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



