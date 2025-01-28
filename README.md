<div align="center"> 
    <h2> Machine Analysis <code>API</code> 💻 </h2>
</div>

#

> [!NOTE]
> This mini project was done as an assessment for [`Unitial Tech`](https://www.unitial.tech/).

<div align="center">

<table>
  <tr>
    <td><strong>CI</strong></td>
    <td>
      <a href="https://github.com/mohammadzainabbas/unitial-assessment/actions/workflows/ci.yml">
        <img src="https://github.com/mohammadzainabbas/unitial-assessment/actions/workflows/ci.yml/badge.svg" alt="CI">
      </a>
    </td>
  </tr>
  <tr>
    <td><strong>Meta</strong></td>
    <td>
      <a href="https://github.com/mohammadzainabbas/unitial-assessment">
        <img src="https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg" alt="Hatch project">
      </a>
      <a href="https://github.com/astral-sh/uv">
        <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
      </a>
      <a href="https://github.com/python/mypy">
        <img src="https://img.shields.io/badge/types-Mypy-blue.svg" alt="types - Mypy">
      </a>
      <a href="https://spdx.org/licenses/">
        <img src="https://img.shields.io/badge/license-MIT-9400d3.svg" alt="License - MIT">
      </a>
    </td>
  </tr>
</table>

</div>

> [!IMPORTANT]
>  This repository contains code for a REST API for processing machines' data and calculating operational KPIs. The API provides the following functionalities:
>
> - [x] Average start/end times per machine
> - [x] Total operational hours
> - [x] Fuel/electricity consumption analysis
> - [x] Peak consumption day detection
> - [x] Efficiency rankings

#

## Getting Started

### Prerequisites

You need one of the following tools to run this project

- Install [`docker`](https://docs.docker.com/get-docker/)
- Install [`uv`](https://docs.astral.sh/uv/getting-started/installation/)

### Clone the repository

```bash
gh repo clone mohammadzainabbas/unitial-assessment
cd unitial-assessment/
```

or 

```bash
git clone https://github.com/mohammadzainabbas/unitial-assessment.git
cd unitial-assessment/
```

### Run the Server

In order to run the server with `uv`, you need to run the following command:

```bash
uv sync
uv run -- uvicorn app.main:app --host 0.0.0.0 --port 8000
```

or with `docker`:

```bash
docker build -t unitial-assessment .
docker run --rm -p 8000:8000 unitial-assessment
```

## API Usage

### Documentation

After running the server, you can access the API documentation at [`http://localhost:8000/docs`](http://localhost:8000/docs).

### Examples

In order to analyze the machines' data, you need to provide the machines' data and the data to be analyzed. The data should be in `json` format. Refer to the following examples to see how to use the API.

> [!CAUTION]
> `curl` and `jq` are required to run the following commands.

1. Simple json data:

Request:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "machines": [
      {
        "id": "9174277a",
        "manufacturer": "Caterpillar",
        "type": "excavator",
        "fuel_type": "electric",
        "battery_size": 115
      }
    ],
    "data": [
      {
        "timestamp": 1683105330180,
        "machine_id": "9174277a",
        "battery_SoC": 0.7795528149
      },
      {
        "timestamp": 1683105335180,
        "machine_id": "9174277a",
        "battery_SoC": 0.7000000000
      }
    ]
  }' \
  http://127.0.0.1:8000/analyze
```

Response:

```json
{
  "machine_metrics": [
    {
      "machine_id": "9174277a",
      "average_start": "09:15:00",
      "average_end": "09:15:00",
      "total_hours": 0.0,
      "consumption": 9.15
    }
  ],
  "peak_consumption_days": { "diesel": null, "electric": "2023-05-03" },
  "efficiency_metrics": {
    "most_efficient": null,
    "least_efficient": null,
    "avg_consumption_per_hour": 0
  }
}
```

2. Use `machines.json` and `data.json` files:

> [!CAUTION]
> Make sure that `machines.json` and `data.json` are in current directory, before running the following `curl` command.

Request:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d "$(jq -s '{machines:.[0], data:.[1]}' machines.json data.json)" \
  http://127.0.0.1:8000/analyze
```

Response:

```json
{
  "machine_metrics": [
    {
      "machine_id": "9174277a",
      "average_start": "07:03:00",
      "average_end": "16:06:00",
      "total_hours": 45.32,
      "consumption": 495.67
    },
    {
      "machine_id": "ab13141f",
      "average_start": "06:08:00",
      "average_end": "16:03:00",
      "total_hours": 49.6,
      "consumption": 1567.93
    },
    {
      "machine_id": "fdf0c409",
      "average_start": "07:02:00",
      "average_end": "16:08:00",
      "total_hours": 43.48,
      "consumption": 158.82
    },
    {
      "machine_id": "06c13c84",
      "average_start": "07:03:00",
      "average_end": "16:01:00",
      "total_hours": 46.89,
      "consumption": 846.04
    },
    {
      "machine_id": "3771cc43",
      "average_start": "06:11:00",
      "average_end": "16:10:00",
      "total_hours": 47.89,
      "consumption": 1148.59
    },
    {
      "machine_id": "39094f50",
      "average_start": "07:07:00",
      "average_end": "15:05:00",
      "total_hours": 40.84,
      "consumption": 101.92
    },
    {
      "machine_id": "65b825ac",
      "average_start": "07:01:00",
      "average_end": "15:02:00",
      "total_hours": 43.11,
      "consumption": 253.29
    },
    {
      "machine_id": "174d96d9",
      "average_start": "06:10:00",
      "average_end": "16:04:00",
      "total_hours": 49.55,
      "consumption": 1704.71
    },
    {
      "machine_id": "046a1338",
      "average_start": "07:10:00",
      "average_end": "17:01:00",
      "total_hours": 47.27,
      "consumption": 786.17
    },
    {
      "machine_id": "72f3c167",
      "average_start": "06:08:00",
      "average_end": "16:02:00",
      "total_hours": 46.49,
      "consumption": 504.87
    },
    {
      "machine_id": "f0a69475",
      "average_start": "07:07:00",
      "average_end": "15:08:00",
      "total_hours": 43.05,
      "consumption": 636.68
    },
    {
      "machine_id": "7a13af83",
      "average_start": "07:08:00",
      "average_end": "16:02:00",
      "total_hours": 46.51,
      "consumption": 797.26
    },
    {
      "machine_id": "b878cb5b",
      "average_start": "06:09:00",
      "average_end": "16:01:00",
      "total_hours": 45.36,
      "consumption": 115.5
    },
    {
      "machine_id": "b151f3cf",
      "average_start": "06:07:00",
      "average_end": "15:07:00",
      "total_hours": 46.06,
      "consumption": 2221.45
    },
    {
      "machine_id": "8645afde",
      "average_start": "07:09:00",
      "average_end": "15:11:00",
      "total_hours": 42.12,
      "consumption": 199.64
    },
    {
      "machine_id": "3ec3e26c",
      "average_start": "07:07:00",
      "average_end": "16:08:00",
      "total_hours": 45.03,
      "consumption": 1716.9
    },
    {
      "machine_id": "43215c19",
      "average_start": "07:05:00",
      "average_end": "15:08:00",
      "total_hours": 44.24,
      "consumption": 860.18
    },
    {
      "machine_id": "38de4d48",
      "average_start": "07:04:00",
      "average_end": "16:10:00",
      "total_hours": 43.55,
      "consumption": 487.3
    },
    {
      "machine_id": "ae6a5a84",
      "average_start": "06:06:00",
      "average_end": "16:04:00",
      "total_hours": 46.78,
      "consumption": 1870.94
    },
    {
      "machine_id": "9e69c463",
      "average_start": "06:06:00",
      "average_end": "16:05:00",
      "total_hours": 46.98,
      "consumption": 454.91
    }
  ],
  "peak_consumption_days": { "diesel": "2023-05-01", "electric": "2023-05-03" },
  "efficiency_metrics": {
    "most_efficient": "b151f3cf",
    "least_efficient": "39094f50",
    "avg_consumption_per_hour": 18.22
  }
}
```