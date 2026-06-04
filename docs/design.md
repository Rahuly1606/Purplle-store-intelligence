# DESIGN.md

# Store Intelligence Platform Design

## Objective

The goal of this system is to convert raw retail surveillance video into actionable store analytics.

The platform detects visitors, tracks movement across the store, generates customer journey events, and computes business metrics such as dwell time, conversion rates, occupancy, and visitor paths.

---

# System Architecture

The system follows a modular pipeline architecture.

```text
Video Input
    ↓
Person Detection
    ↓
Multi-Object Tracking
    ↓
Zone Assignment
    ↓
State Management
    ↓
Event Generation
    ↓
Analytics Engine
    ↓
Reports & Visualizations
```

Each stage is independent and can be replaced without affecting the rest of the pipeline.

---

# Detection Layer

## YOLOv8

YOLOv8 is used for person detection.

Responsibilities:

* Detect people in each frame
* Generate bounding boxes
* Provide confidence scores

Output:

```json
{
  "track_id": 1,
  "bbox": [x1, y1, x2, y2],
  "confidence": 0.91
}
```

---

# Tracking Layer

## ByteTrack

ByteTrack assigns consistent IDs across frames.

Responsibilities:

* Maintain visitor identity
* Reduce duplicate counting
* Enable dwell and path analytics

Example:

```text
Frame 1   → Person #1
Frame 50  → Person #1
Frame 100 → Person #1
```

---

# Zone Assignment

Store zones are configured in:

```text
config/zones.json
```

Example:

```json
{
  "FOH": [600, 350, 1450, 950]
}
```

A visitor's zone is determined using the feet point of the bounding box.

Reason:

The feet point is a better approximation of floor position than the bounding box center.

---

# Zone Stabilization

## Hysteresis Manager

Detection noise can cause rapid zone switching near boundaries.

A hysteresis layer confirms a zone transition only after multiple consecutive observations.

Benefits:

* Reduces flickering
* Produces stable customer paths
* Improves analytics quality

---

# State Management

The StateManager maintains visitor lifecycle information.

Responsibilities:

* Visitor confirmation
* Zone tracking
* Entry generation
* Zone transition generation

Generated events:

* ENTRY
* EXIT
* ZONE_ENTER
* ZONE_EXIT

---

# Event Streaming

Events are written as JSONL.

Advantages:

* Simple format
* Append-only
* Easy analytics processing
* Human-readable

Example:

```json
{
  "visitor_id": "VIS_1",
  "event_type": "ZONE_ENTER",
  "zone_id": "ALPS"
}
```

---

# Analytics Layer

The analytics subsystem consumes generated events.

Modules include:

* Dwell Analytics
* Funnel Analytics
* Path Analytics
* Occupancy Analytics
* Staff Classification

Each module operates independently.

---

# Visualization Layer

The platform generates:

## Heatmap

Displays customer engagement intensity.

## Annotated Video

Displays:

* Bounding boxes
* Visitor IDs
* Zone labels
* Staff/Customer classification

---

# Reporting Layer

The final report aggregates:

* Visitor counts
* Zone visits
* Dwell times
* Conversion rates
* Occupancy statistics
* Customer journeys

Output:

```text
outputs/final_report.json
```

---

# Scalability Considerations

Future enhancements:

* Multi-camera tracking
* Real-time processing
* Kafka event streaming
* Cloud deployment
* Dashboard integration

The current architecture is intentionally modular to support these extensions with minimal code changes.
