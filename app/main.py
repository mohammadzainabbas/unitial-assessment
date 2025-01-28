from datetime import datetime
from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Machine Data Analysis API", version="0.1.0")

class Machine(BaseModel):
    id: str
    manufacturer: str
    type: str
    fuel_type: str
    battery_size: Optional[int] = None
    fuel_tank_size: Optional[int] = None

class DataPoint(BaseModel):
    timestamp: int
    machine_id: str
    fuel_level: Optional[float] = None
    battery_SoC: Optional[float] = None

@app.post("/api/analyze")
def analyze_data(machines: List[Machine] = Body(...), data: List[DataPoint] = Body(...)):
    """
    Ingestes the machine (machines.json) and data (data.json) arrays,
    performs basic analysis, and returns a result summary.
    """

    # Map machines by ID
    machine_map = {m.id: m for m in machines}

    # Group data by machine ID
    machines_data = {}
    for d in data:
        if d.machine_id not in machine_map:
            # Skip unknown machines if present
            continue
        machines_data.setdefault(d.machine_id, []).append(d)

    results = []
    daily_consumption_diesel = {}
    daily_consumption_electric = {}

    for mid, points in machines_data.items():
        # Sort points by timestamp
        points.sort(key=lambda x: x.timestamp)
        start_ts = points[0].timestamp
        end_ts = points[-1].timestamp

        # Hours worked is naive difference between earliest and latest data points
        hours_worked = (end_ts - start_ts) / 3600000.0  # from ms to hours

        machine_info = machine_map[mid]
        consumption = 0.0
        # We'll assume consumption is difference in SoC/fuel between first and last reading * capacity
        first = points[0]
        last = points[-1]

        if machine_info.fuel_type == "diesel" and machine_info.fuel_tank_size:
            if first.fuel_level is not None and last.fuel_level is not None:
                consumption = (first.fuel_level - last.fuel_level) * machine_info.fuel_tank_size
                consumption = max(consumption, 0)  # clamp if negative
        elif machine_info.fuel_type == "electric" and machine_info.battery_size:
            if first.battery_SoC is not None and last.battery_SoC is not None:
                consumption = (first.battery_SoC - last.battery_SoC) * machine_info.battery_size
                consumption = max(consumption, 0)

        # Tally daily consumption
        for p in points:
            day_str = datetime.utcfromtimestamp(p.timestamp/1000).strftime("%Y-%m-%d")
            if machine_info.fuel_type == "diesel":
                daily_consumption_diesel.setdefault(day_str, 0.0)
                # approximate delta per data point (very naive)
                daily_consumption_diesel[day_str] += consumption / len(points)
            else:
                daily_consumption_electric.setdefault(day_str, 0.0)
                daily_consumption_electric[day_str] += consumption / len(points)

        # Calculate average start and end time
        avg_start_time = datetime.utcfromtimestamp(start_ts/1000).isoformat()
        avg_end_time = datetime.utcfromtimestamp(end_ts/1000).isoformat()

        results.append({
            "machine_id": mid,
            "hours_worked": round(hours_worked, 2),
            "avg_start_time": avg_start_time,
            "avg_end_time": avg_end_time,
            "consumption": round(consumption, 2),
            "consumption_unit": "kWh" if machine_info.fuel_type == "electric" else "L"
        })

    highest_diesel = max(daily_consumption_diesel, key=daily_consumption_diesel.get) if daily_consumption_diesel else None
    highest_electric = max(daily_consumption_electric, key=daily_consumption_electric.get) if daily_consumption_electric else None

    return {
        "analysis": results,
        "day_highest_diesel_consumption": highest_diesel,
        "day_highest_electric_consumption": highest_electric
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}
