from pydantic import BaseModel
from typing import Optional, List

class MachineSchema(BaseModel):
    id: str
    manufacturer: str
    type: str
    fuel_type: str
    battery_size: Optional[int] = None
    fuel_tank_size: Optional[int] = None

class DataEntrySchema(BaseModel):
    timestamp: int
    machine_id: str
    fuel_level: Optional[float] = None
    battery_SoC: Optional[float] = None

class AnalysisResponse(BaseModel):
    machine_metrics: List[dict]
    peak_consumption_days: dict
    efficiency_metrics: dict