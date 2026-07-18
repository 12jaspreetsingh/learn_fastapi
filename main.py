from fastapi import FastAPI,Path,HTTPException,Query
import json
from typing import Dict,Annotated,Literal,Optional
from pydantic import BaseModel, ValidationError, EmailStr, Field, field_validator, model_validator, computed_field
app = FastAPI()
class Patient(BaseModel):
    id: Annotated[str, Field(..., description="The ID of the patient")]
    name: Annotated[str, Field(..., description="The name of the patient")]
    city: Annotated[str, Field(..., description="The city of the patient")]
    age: Annotated[int, Field(...,gt=0,lt=120, description="The age of the patient")]
    gender: Annotated[Literal["male", "female", "other"], Field(..., description="The gender of the patient")]
    height: Annotated[float, Field(..., gt=0,lt=2.5, description="The height of the patient in meters")]
    weight: Annotated[float, Field(...,gt=0,lt=300, description="The weight of the patient in kilograms")] 

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)         
    @computed_field
    @property
    def bmi_category(self) -> str:
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(None, description="The name of the patient")]
    city: Annotated[Optional[str], Field(None, description="The city of the patient")]
    age: Annotated[Optional[int], Field(None, gt=0, lt=120, description="The age of the patient")]
    gender: Annotated[Optional[Literal["male", "female", "other"]], Field(None, description="The gender of the patient")]
    height: Annotated[Optional[float], Field(None, gt=0, lt=2.5, description="The height of the patient in meters")]
    weight: Annotated[Optional[float], Field(None, gt=0, lt=300, description="The weight of the patient in kilograms")]


def load_data():
    # Placeholder for data loading logic
    with open("patients.json", "r") as file:
        data = json.load(file)
    return data

@app.get("/")
def hello():
    return {"message": "Patient management system is running."} 
@app.get("/about")
def about():
    return {"message": "A fully functional patient management system built with FastAPI."}
@app.get("/view")
def view():
    data = load_data()
    return {"patients": data}
@app.get("/patient/{patient_id}")
def view_patient(patient_id: str=Path(..., description="The ID of the patient to retrieve",example="P001")):
    data = load_data()

    patient = data.get(patient_id)

    if patient:
        return {"patient": patient}

    raise HTTPException(status_code=404, detail="Patient not found")
@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="The field to sort patients by height,weight,bmi"), order: str = Query("asc", description="The order to sort patients by", example="asc")):
    data = load_data()
    valid_sort_fields = ["height", "weight", "bmi"]
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid sort order")
    sorted_patients = dict(sorted(data.items(), key=lambda item: item[1][sort_by], reverse=(order == "desc")))
    return {"sorted_patients": sorted_patients}
@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")
    data[patient.id] = patient.model_dump()
    with open("patients.json", "w") as file:
        json.dump(data, file, indent=4)
    return {"message": "Patient created successfully", "patient": patient.model_dump()}
@app.put("/edit/{patient_id}")
def edit_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    existing_patient_info = data[patient_id]
    updated_patient_data = existing_patient_info.copy()
    update_data = patient_update.model_dump(exclude_unset=True)
    updated_patient_data.update(update_data)
    updated_patient_data['id'] = patient_id  # Ensure the error is not raised by including the 'id' field in the updated data
    updated_patient = Patient(**updated_patient_data)
    data[patient_id] = updated_patient.model_dump()
    print(updated_patient.model_dump())
    with open("patients.json", "w") as file:   
        json.dump(data, file, indent=4)
        print("Saved!")
    return {"message": "Patient updated successfully", "patient": updated_patient.model_dump()}