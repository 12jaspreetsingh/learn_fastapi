from pydantic import BaseModel, ValidationError,EmailStr,Field,field_validator
from typing import Optional,List,Dict,Annotated
class Patient(BaseModel):
    name: Annotated[str, Field(..., description="The name of the patient in less than 100 characters", max_length=100)]
    email: Optional[EmailStr] = None
    age: int = Field(..., gt=0,lt=120) 
    weight: float = Field(None, gt=0,strict=True)
    married: bool = Field(None)
    allergies: List[str] = Field(None)
    contact: Dict[str,str] = Field(None)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        valid_domain=['hdfc.com','gmail.com','yahoo.com']
        domain_name=v.split('@')[-1]
        if domain_name not in valid_domain:
            raise ValueError("Invalid email domain")
        return v
    @field_validator('name')
    @classmethod
    def transform_name(cls, v):
        return v.upper()  # Capitalize the first letter of each word in the name

patient_info={'name': 'John Doe', 'email': 'john.doe@gmail.com', 'age': 50, 'weight': 70.5,'married': False}  # Example data with age as an integer and weight as a float
patient1=Patient(**patient_info)  # This will create a valid Patient instance
def insert_patient_data(patient:Patient):
    """
    Inserts patient data into the database.

    Args:
        name (str): The name of the patient.
        age (int): The age of the patient.
        weight (float): The weight of the patient.
        married (bool): The marital status of the patient.
        allergies (List[str]): The allergies of the patient.
        contact (Dict[str,str]): The contact information of the patient.

    Returns:
        bool: True if insertion was successful, False otherwise.
    """
    try:
        # Assuming we have a database connection and a patients table
        # This is a placeholder for actual database insertion logic
        # db.insert('patients', patient_data)
        print(patient.name, patient.email, patient.age,patient.weight,patient.married,patient.allergies,patient.contact)                     
        return True
    except Exception as e:
        print(f"Error inserting patient data: {e}")
        return False
def update_patient_data(patient:Patient):
    """
    Updates patient data in the database.


    Args:
        name (str): The name of the patient.
        age (int): The age of the patient.

    Returns:
        bool: True if update was successful, False otherwise.
    """
    try:
        # Assuming we have a database connection and a patients table
        # This is a placeholder for actual database update logic
        # db.update('patients', patient_data)
        print(patient.name, patient.age,patient.weight,patient.married,patient.allergies,patient.contact)                     
        return True
    except Exception as e:
        print(f"Error updating patient data: {e}")
        return False
insert_patient_data(patient1)  # Example usage of the function with a string for age, which should be an integer.
