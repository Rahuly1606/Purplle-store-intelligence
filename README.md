# Store Intelligence Platform

## Overview

Store Intelligence Platform is a computer vision and retail analytics system designed to transform raw CCTV footage into actionable business insights.

The system automatically detects visitors, tracks movement across the store, identifies zone interactions, generates customer journey events, computes dwell-time analytics, measures conversion funnels, estimates occupancy, classifies probable staff members, and produces visual outputs such as heatmaps and annotated videos.

The platform is built using a modular architecture, making it easy to extend, maintain, and deploy.

---

# Key Features

## Visitor Detection

* YOLOv8-based person detection
* Real-time inference
* Confidence filtering
* Small-object suppression

## Visitor Tracking

* ByteTrack multi-object tracking
* Persistent visitor IDs
* Reduced duplicate counting
* Stable visitor trajectories

## Zone Intelligence

* Configurable store zones
* Feet-point based zone assignment
* Zone transition detection
* Hysteresis-based stabilization

## Event Generation

Generated events:

* ENTRY
* EXIT
* ZONE_ENTER
* ZONE_EXIT

Events are stored as JSONL records for downstream analytics.

## Dwell Analytics

Measures:

* Time spent in each zone
* Average dwell time per zone
* Customer engagement levels

## Funnel Analytics

Tracks customer movement between key zones.

Example:

```text
FOH → CASH_COUNTER
```

## Visitor Journey Analytics

Tracks complete visitor movement paths.

Example:

```text
FOH → ALPS → MENS_CARE → CASH_COUNTER
```

## Occupancy Analytics

Tracks:

* Current occupancy
* Peak occupancy
* Zone crowding behavior

## Staff Classification

Heuristic-based identification of probable staff members using long dwell behavior.

## Heatmap Generation

Creates visual heatmaps showing customer engagement hotspots.

## Annotated Video Generation

Produces videos containing:

* Bounding boxes
* Visitor IDs
* Zone labels
* Staff/Customer labels

## Final Reporting

Generates a consolidated report containing all analytics and metrics.

## Store Intelligence Dashboard

Interactive Streamlit dashboard for visualizing all analytics.

Displays:

* Executive KPI overview
* Dwell time analytics
* Zone visit counts
* Conversion funnel
* Peak occupancy
* Visitor journeys
* Customer engagement heatmap
* Annotated video playback
* Raw report viewer

---

# System Architecture

```text
Input Video
     │
     ▼
YOLOv8 Detection
     │
     ▼
ByteTrack Tracking
     │
     ▼
Zone Assignment
     │
     ▼
State Management
     │
     ▼
Event Generation
     │
     ▼
Analytics Layer
     │
     ├── Dwell Analytics
     ├── Funnel Analytics
     ├── Path Analytics
     ├── Occupancy Analytics
     └── Staff Classification
     │
     ▼
Visualization Layer
     │
     ├── Heatmap
     └── Annotated Video
     │
     ▼
Final Report
     │
     ▼
Streamlit Dashboard
```

---

# Project Structure

```text
Store-Intelligence/

├── config/
│   └── zones.json
│
├── dashboard/
│   ├── app.py
│   ├── charts.py
│   └── utils.py
│
├── data/
│   ├── videos/
│   │   └── sample.mp4
│   │
│   └── events/
│       └── generated_events.jsonl
│
├── docs/
│   ├── design.md
│   └── choices.md
│
├── outputs/
│   ├── heatmap.png
│   ├── annotated_store_video.mp4
│   ├── store_metrics.json
│   └── final_report.json
│
├── pipeline/
│   ├── analytics/
│   ├── detection/
│   ├── events/
│   ├── reporting/
│   ├── visualization/
│   └── zones/
│
├── tools/
│
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# Prerequisites

## Software

* Python 3.10+
* Docker Desktop
* Git

## Hardware

Recommended:

* 8 GB RAM minimum
* 16 GB RAM preferred
* NVIDIA GPU (optional)

Verify installation:

```bash
python --version
pip --version
docker --version
git --version
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd Store-Intelligence
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Input Requirements

The following files must exist before execution:

```text
config/zones.json
data/videos/sample.mp4
yolov8n.pt
```

## Video Requirements

Recommended:

* MP4 format
* 1080p resolution
* Fixed camera angle
* Retail store environment

---

# Zone Configuration

Store zones are defined in:

```text
config/zones.json
```

Example:

```json
{
  "zones": {
    "FOH": [600, 350, 1450, 950],
    "ALPS": [1160, 950, 1360, 1200],
    "CASH_COUNTER": [1450, 250, 1850, 850]
  }
}
```

Coordinates are represented as:

```text
[x1, y1, x2, y2]
```

---

# Running the Pipeline

## Execute

```bash
python -m pipeline.main_pipeline
```

Expected console output:

```text
Pipeline completed

AVERAGE DWELL TIMES:
FOH: ...
ALPS: ...
CASH_COUNTER: ...

TOTAL VISITORS: X
```

---

# Running the Dashboard

After the pipeline has completed and outputs are generated:

```bash
streamlit run dashboard/app.py
```

The dashboard will open at:

```text
http://localhost:8501
```

## Dashboard Sections

| Section              | Description                          |
| -------------------- | ------------------------------------ |
| Executive Overview   | KPI cards — visitors, conversion     |
| Dwell Analytics      | Average dwell time per zone          |
| Zone Visits          | Visit count per zone                 |
| Conversion Funnel    | FOH → CASH_COUNTER funnel chart      |
| Peak Occupancy       | Maximum concurrent visitors per zone |
| Visitor Journeys     | Searchable visitor path table        |
| Heatmap              | Customer engagement heatmap          |
| Annotated Video      | Inline annotated video playback      |
| Raw Metrics          | Expandable final_report.json viewer  |

---

# Generated Outputs

After successful pipeline execution:

```text
outputs/
├── heatmap.png
├── annotated_store_video.mp4
├── store_metrics.json
└── final_report.json

data/events/
└── generated_events.jsonl
```

---

# Output Descriptions

## generated_events.jsonl

Raw event stream.

Example:

```json
{
  "visitor_id": "VIS_1",
  "event_type": "ZONE_ENTER",
  "zone_id": "ALPS"
}
```

---

## store_metrics.json

Contains:

* Total visitors
* Staff count
* Customer count
* Average dwell times
* Zone visits
* Visitor paths
* Conversion metrics
* Occupancy metrics

---

## final_report.json

Challenge-ready consolidated analytics report.

Contains:

* Visitor statistics
* Zone analytics
* Funnel analytics
* Occupancy analytics
* Journey analytics

---

## heatmap.png

Visual representation of customer engagement across the store.

Used to identify:

* Hot zones
* Dead zones
* Popular shelves

---

## annotated_store_video.mp4

Annotated video containing:

* Bounding boxes
* Visitor IDs
* Zone labels
* Staff/Customer labels

Used for:

* Validation
* Debugging
* Demonstration

---

# Verification Checklist

After execution verify:

* [ ] generated_events.jsonl created
* [ ] store_metrics.json created
* [ ] final_report.json created
* [ ] heatmap.png created
* [ ] annotated_store_video.mp4 created
* [ ] Dashboard loads without errors
* [ ] No runtime errors occurred
* [ ] Visitor count is greater than zero

---

# Docker Build & Verification

## Build Image

```bash
docker build -t store-intelligence .
```

## Verify Build

```bash
docker images
```

Expected:

```text
store-intelligence   latest
```

---

## Run Container

```bash
docker run --rm store-intelligence
```

---

## Run With Mounted Volumes

### Windows PowerShell

```powershell
docker run --rm `
-v ${PWD}/data:/app/data `
-v ${PWD}/outputs:/app/outputs `
store-intelligence
```

### Linux / macOS

```bash
docker run --rm \
-v $(pwd)/data:/app/data \
-v $(pwd)/outputs:/app/outputs \
store-intelligence
```

---

## Verify Outputs

Expected:

```text
outputs/
├── heatmap.png
├── annotated_store_video.mp4
├── store_metrics.json
└── final_report.json
```

---

# Challenge Requirement Mapping

| Requirement              | Implementation       |
| ------------------------ | -------------------- |
| Visitor Detection        | YOLOv8               |
| Visitor Tracking         | ByteTrack            |
| Zone Assignment          | ZoneManager          |
| Entry Detection          | StateManager         |
| Exit Detection           | ExitManager          |
| Dwell Analytics          | DwellEngine          |
| Visitor Journey Tracking | PathAnalyzer         |
| Funnel Analytics         | FunnelAnalyzer       |
| Occupancy Analytics      | OccupancyAnalyzer    |
| Staff Detection          | StaffClassifier      |
| Heatmap Generation       | HeatmapGenerator     |
| Video Annotation         | VideoAnnotator       |
| Final Reporting          | FinalReportGenerator |
| Analytics Dashboard      | Streamlit Dashboard  |

---

# Assumptions

1. Single-camera retail environment.
2. One track ID corresponds to one visitor.
3. Zone boundaries are manually configured.
4. Staff members generally remain longer in specific zones.
5. Videos may end before all visitors leave the store.
6. Analytics are generated only from observable video evidence.
7. Camera position remains fixed.

---

# Design Documents

Additional documentation:

```text
README.md          → Setup and execution
docs/design.md     → System architecture
docs/choices.md    → Engineering decisions and tradeoffs
```

---

# Technologies Used

* Python
* OpenCV
* YOLOv8
* ByteTrack
* NumPy
* JSONL
* Docker
* Streamlit
* Plotly
* Pandas

---

# Future Enhancements

* Appearance-based Re-Identification
* Multi-camera tracking
* Queue analytics
* Shelf interaction analytics
* Real-time dashboard
* Kafka event streaming
* Cloud deployment
* Alert generation

---

# Deliverables

Final generated artifacts:

```text
generated_events.jsonl
store_metrics.json
final_report.json
heatmap.png
annotated_store_video.mp4
```

Dashboard:

```text
streamlit run dashboard/app.py
```

These artifacts provide both machine-readable analytics and human-verifiable evidence of store activity and visitor behavior.
