from datetime import datetime, time
from collections import defaultdict
from typing import List, Dict, Any
from app.models.schemas import MachineSchema, DataEntrySchema

def process_analysis(machines: List[MachineSchema], data: List[DataEntrySchema]) -> Dict[str, Any]:
    machine_data = defaultdict(list)
    for entry in data:
        machine_data[entry.machine_id].append(entry)

    metrics = [calculate_machine_metrics(m, machine_data[m.id]) for m in machines]
    efficiency = calculate_efficiency_metrics(metrics)

    return {
        "machine_metrics": metrics,
        "peak_consumption_days": calculate_peak_consumption(machines, data),
        "efficiency_metrics": efficiency,
    }

def calculate_machine_metrics(machine: MachineSchema, entries: List[DataEntrySchema]) -> dict:
    sorted_entries = sorted(entries, key=lambda e: e.timestamp)
    start, end, hours = time_metrics(sorted_entries)
    consumption = calculate_consumption(machine, sorted_entries)

    return {
        "machine_id": machine.id,
        "average_start": start.isoformat() if start else None,
        "average_end": end.isoformat() if end else None,
        "total_hours": round(hours, 2),
        "consumption": consumption,
    }

def time_metrics(entries: List[DataEntrySchema]) -> tuple:
    if not entries:
        return None, None, 0.0

    daily = defaultdict(list)
    for e in entries:
        dt = datetime.fromtimestamp(e.timestamp / 1000)
        daily[dt.date()].append(e)

    starts, ends, total = [], [], 0
    for day in daily.values():
        day_sorted = sorted(day, key=lambda x: x.timestamp)
        start = day_sorted[0].timestamp
        end = day_sorted[-1].timestamp
        starts.append(datetime.fromtimestamp(start / 1000).time())
        ends.append(datetime.fromtimestamp(end / 1000).time())
        total += end - start

    avg_start = average_time(starts) if starts else None
    avg_end = average_time(ends) if ends else None
    return avg_start, avg_end, total / 3_600_000

def calculate_consumption(machine: MachineSchema, entries: List[DataEntrySchema]) -> float:
    capacity = machine.battery_size or machine.fuel_tank_size or 0
    prev = None
    total = 0.0

    for e in sorted(entries, key=lambda x: x.timestamp):
        level = e.battery_SoC if machine.fuel_type == "electric" else e.fuel_level
        if level is not None and prev is not None and level < prev:
            total += (prev - level) * capacity
        prev = level

    return round(total, 2)

def calculate_efficiency_metrics(metrics: List[dict]) -> dict:
    efficiencies = []
    for m in metrics:
        if m["total_hours"] > 0:
            eff = m["consumption"] / m["total_hours"]
            efficiencies.append((m["machine_id"], eff))

    return {
        "most_efficient": max(efficiencies, key=lambda x: x[1])[0]
        if efficiencies
        else None,
        "least_efficient": min(efficiencies, key=lambda x: x[1])[0]
        if efficiencies
        else None,
        "avg_consumption_per_hour": round(sum(x[1] for x in efficiencies) / len(efficiencies), 2)
        if efficiencies
        else 0,
    }

def calculate_peak_consumption(machines: List[MachineSchema], data: List[DataEntrySchema]) -> dict:
    diesel = defaultdict(float)
    electric = defaultdict(float)

    for m in machines:
        entries = [e for e in data if e.machine_id == m.id]
        capacity = m.battery_size or m.fuel_tank_size or 0
        prev = None

        for e in sorted(entries, key=lambda x: x.timestamp):
            level = e.battery_SoC if m.fuel_type == "electric" else e.fuel_level
            date = datetime.fromtimestamp(e.timestamp / 1000).date()

            if level is not None and prev is not None and level < prev:
                consumption = (prev - level) * capacity
                if m.fuel_type == "electric":
                    electric[date] += consumption
                else:
                    diesel[date] += consumption
            prev = level

    return {
        "diesel": max(diesel, key=diesel.get, default=None),
        "electric": max(electric, key=electric.get, default=None),
    }

def average_time(times: List[time]) -> time:
    total = sum(t.hour * 3600 + t.minute * 60 + t.second for t in times)
    return time.fromisoformat(
        f"{int(total // 3600 // len(times)):02d}:{int((total % 3600) // 60 // len(times)):02d}"
    )
