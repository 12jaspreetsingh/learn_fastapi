from fastapi import FastAPI,Path,HTTPException,Query
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