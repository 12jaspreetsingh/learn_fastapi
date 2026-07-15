from fastapi import FastAPI,Path,HTTPException
import json
app = FastAPI()
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