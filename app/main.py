from fastapi import FastAPI
from app.models.schemas import AnalysisResponse, MachineSchema, DataEntrySchema
from app.processing.analysis import process_analysis

app = FastAPI(title="Machine Analysis API", version="0.1")

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(machines: list[MachineSchema], data: list[DataEntrySchema]):
    return process_analysis(machines, data)

@app.get("/")
async def root():
    return {"message": "Hello from the Machine Analysis API!"}