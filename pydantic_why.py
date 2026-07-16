from pydantic import BaseModel, ValidationError
class Patient(BaseModel):
    name: str
    age: int
patient_info={'name': 'John Doe', 'age': 50}  # Example data with age as an integer
patient1=Patient(**patient_info)  # This will create a valid Patient instance
def insert_patient_data(patient:dict):
    """
    Inserts patient data into the database.

    Args:
        name (str): The name of the patient.
        age (int): The age of the patient.

    Returns:
        bool: True if insertion was successful, False otherwise.
    """
    try:
        # Assuming we have a database connection and a patients table
        # This is a placeholder for actual database insertion logic
        # db.insert('patients', patient_data)
        print(patient.name, patient.age)                     
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
        print(patient.name, patient.age)                     
        return True
    except Exception as e:
        print(f"Error updating patient data: {e}")
        return False
update_patient_data(patient1)  # Example usage of the function with a string for age, which should be an integer.
