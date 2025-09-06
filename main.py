import httpx
from fastapi import FastAPI
from pydantic import BaseModel,Field
from typing import List,Dict

# https://github.com/7-solutions/frontend-assignment
# https://docs.pydantic.dev/2.3/usage/types/dicts_mapping/

example_url = "https://dummyjson.com/users"

class Coordinates(BaseModel):
    lat : float
    lng :float

class Address(BaseModel):
    address : str
    city : str
    state : str
    stateCode : str
    postalCode : str
    coordinates : Coordinates
    country : str

class Hair(BaseModel):
    color : str
    type : str

class Bank(BaseModel):
   cardExpire : str 
   cardNumber : str 
   cardType : str 
   currency : str 
   iban : str 

class Company(BaseModel):
    department : str 
    name : str 
    title : str 
    address : Address

class Crypto(BaseModel):
    coin : str 
    wallet : str 
    network : str 

class User(BaseModel):
    id : int
    firstName : str
    lastName : str
    maidenName : str
    age : int
    gender : str
    email : str
    phone : str
    username : str
    password : str
    birthDate : str
    image : str
    bloodGroup : str
    height : float
    weight : float
    eyeColor : str
    hair : Hair
    ip : str
    address : Address
    macAddress : str
    university : str
    bank : Bank
    company : Company
    ein : str
    ssn : str
    userAgent : str
    crypto : Crypto
    role : str

class Summary(BaseModel):
    male : int = Field(default=0)
    female : int = Field(default=0)
    ageRange : str
    hair : Dict[str,int] = Field(default_factory=dict)
    addressUser: Dict[str,str] = Field(default_factory=dict)

app = FastAPI()

@app.get("/")
def root():
    return {"message":"adkaldkflskds"}

@app.get("/users",response_model=list[User])
async def get_users():
    summaries = {}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(example_url)
            response.raise_for_status()
            json = response.json()
            users : List[User] = [User(**user) for user in json['users']]
            for user in users:
                update_summary(user,summaries)

            print(summaries)
            return users
        except httpx.HTTPStatusError as exc:
            print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
            return {"error": f"API request failed with status {exc.response.status_code}"}
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"error": "An unexpected error occurred"}

def update_summary(user:User,summaries:dict):
    # check department is exist in summariess
    if user.company.department not in summaries:
        summaries[user.company.department] = Summary()
    update_departmant(user,summaries[user.company.department])

def update_departmant(user:User,department:dict):
    print(department)