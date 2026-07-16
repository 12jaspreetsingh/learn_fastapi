from pydantic import BaseModel, ValidationError, EmailStr, Field, field_validator, model_validator,computed_field
from typing import Optional, List, Dict, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(description="The name of the patient in less than 100 characters", max_length=100)]
    email: Optional[EmailStr] = None
    age: int = Field(..., gt=0, lt=100) # Adjusted to match your validator intent
    weight: Optional[float] = Field(None, gt=0, strict=True)
    height: Optional[float] = Field(None, gt=0, strict=True)
    married: Optional[bool] = None
    allergies: Optional[List[str]] = None
    contact: Optional[Dict[str, str]] = None
    
    @computed_field
    @property
    def bmi(self) -> Optional[float]:
        if self.weight and self.height:
            return round(self.weight / ((self.height / 100) ** 2), 2)
        return None
    @model_validator(mode='after')
    def validate_patient(self):
        # Prevent crash if contact is None
        if self.age > 60:
            if not self.contact or 'emergency' not in self.contact:
                raise ValueError("Emergency contact is required for patients over 60")
        return self

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if v: # Only validate if email is actually provided
            valid_domains = ['hdfc.com', 'gmail.com', 'yahoo.com']
            domain_name = v.split('@')[-1]
            if domain_name not in valid_domains:
                raise ValueError("Invalid email domain")
        return v

    @field_validator('name')
    @classmethod
    def transform_name(cls, v):
        return v.upper() 

    @field_validator('age', mode='after')
    @classmethod
    def validate_age(cls, v):
        if 0 < v < 100:
            return v
        raise ValueError("Age must be between 0 and 100")

# 'age' as a string '50' works because Pydantic automatically parses it to an int!
patient_info = {
    'name': 'John Doe', 
    'email': 'john.doe@gmail.com', 
    'age': '50', 
    'weight': 70.5, 
    'height': 175.0,
    'married': False
}  

try:
    patient1 = Patient(**patient_info)
    
    def insert_patient_data(patient: Patient):
        print(patient.name, patient.email, patient.age, patient.weight, patient.height, patient.married, patient.allergies, patient.contact,patient.bmi)                     
        return True

    insert_patient_data(patient1)
    
except ValidationError as e:
    print(e)