# CHOICES.md

# Technical Choices and Tradeoffs

This document explains the major design decisions made during development and the reasoning behind each choice.

---

# Why YOLOv8?

Alternative options:

* Faster R-CNN
* SSD
* YOLOv5
* YOLOv7

Chosen:

YOLOv8

Reasons:

* Excellent real-time performance
* Strong detection accuracy
* Simple integration
* Active community support

Tradeoff:

Slightly lower accuracy than larger models, but significantly faster inference.

---

# Why ByteTrack?

Alternative options:

* DeepSORT
* StrongSORT
* OC-SORT

Chosen:

ByteTrack

Reasons:

* High tracking accuracy
* Robust ID persistence
* Lightweight
* Easy deployment

Tradeoff:

Does not provide appearance-based re-identification.

---

# Why Feet Point Instead of Bounding Box Center?

Alternative:

Bounding box center.

Chosen:

Feet point.

Reason:

Store zones exist on the floor.

The feet point better represents the actual location of a visitor.

Benefits:

* Improved zone accuracy
* Better shelf attribution
* Reduced boundary errors

---

# Why Hysteresis?

Problem:

Tracking noise can create false transitions.

Example:

```text
ALPS
MENS_CARE
ALPS
MENS_CARE
```

within a few frames.

Solution:

Hysteresis-based zone confirmation.

Benefits:

* Stable zone assignments
* Cleaner customer paths
* More reliable dwell analytics

Tradeoff:

Slight delay before accepting a zone change.

---

# Why JSONL Events?

Alternatives:

* SQL database
* CSV files
* Message queues

Chosen:

JSONL

Reasons:

* Simple append-only format
* Human-readable
* Easy debugging
* Easy replay

Tradeoff:

Not optimized for large-scale production workloads.

---

# Why Modular Analytics?

Instead of building one monolithic analytics engine, analytics were separated into independent modules.

Modules:

* DwellAnalyzer
* FunnelAnalyzer
* PathAnalyzer
* OccupancyAnalyzer
* StaffClassifier

Benefits:

* Easier testing
* Easier maintenance
* Independent evolution

---

# Why Rule-Based Staff Classification?

Alternative:

Machine learning classifier.

Chosen:

Rule-based approach.

Reason:

Limited labeled training data.

Benefits:

* Deterministic behavior
* Fast execution
* Explainable results

Tradeoff:

May misclassify unusual visitor behavior.

---

# Why Generate Heatmaps?

Metrics alone are difficult to validate visually.

Heatmaps provide:

* Hotspot detection
* Dead-zone detection
* Customer engagement visualization

Benefits:

Useful for both judges and retail stakeholders.

---

# Why Generate Annotated Videos?

Business metrics should be traceable back to video evidence.

Annotated videos provide:

* Visual verification
* Easier debugging
* Stakeholder confidence

Benefits:

Improves explainability and transparency.

---

# Key Engineering Principles

During implementation the following principles were prioritized:

1. Simplicity over complexity
2. Explainability over black-box behavior
3. Modular architecture
4. Deterministic analytics
5. Challenge-focused implementation
6. Easy reproducibility through Docker

These principles guided all major design decisions throughout the project.
