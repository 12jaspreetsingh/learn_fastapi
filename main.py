from fastapi import FastAPI
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
def view_patient(patient_id: str):
    data = load_data()

    patient = data.get(patient_id)

    if patient:
        return {"patient": patient}

    return {"error": "Patient not found"}