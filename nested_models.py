from pydantic import BaseModel, ValidationError, EmailStr, Field, field_validator, model_validator, computed_field
from typing import Optional, List, Dict, Annotated  
class Address(BaseModel):
    city: str
    state: str
    zip_code: str
class Patient(BaseModel):
    name: Annotated[str, Field(description="The name of the patient in less than 100 characters", max_length=100)]
    age: int = Field(..., gt=0, lt=100) # Adjusted to match your validator intent
    gender :str
    address: Address
address_info = {
    'city': 'New York',
    'state': 'NY',
    'zip_code': '10001'
}
address = Address(**address_info)

patient_info = {
    'name': 'John Doe',
    'age': 30,
    'gender': 'Male',
    'address': address
}
try:
    patient = Patient(**patient_info)
    temp=patient.model_dump_json()
    print(temp)
    print(type(temp))
except ValidationError as e:
    print(e.json())