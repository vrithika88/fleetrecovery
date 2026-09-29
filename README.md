# FleetGuard — Robot Fleet Recovery

## Demo Credentials

> **Username:** `hackfusion`
> **Password:** `yoi time`

> **Note:** These credentials are intended exclusively for accessing the FleetGuard hackathon prototype. Do not use real or production credentials in this repository.

> **Recover the cell before the cascade spreads.**

FleetGuard is a **front-end prototype for resilient robot-fleet operations**, designed around the problem of recovering autonomous robotic systems when individual failures propagate across an interconnected fleet.

The interface conceptualizes a centralized **fleet recovery and operations console** that enables operators to monitor robot health, visualize dependencies, identify cascading failure risks, simulate recovery scenarios, and manually reassign workloads to operational units.

## Overview

In a coordinated robotic fleet, the failure of a single unit can create a chain reaction—disrupting dependent tasks, increasing workload on neighbouring robots, and ultimately compromising overall mission continuity.

FleetGuard addresses this challenge through a unified operational interface focused on:

* **Real-time fleet visibility**
* **Failure propagation analysis**
* **Dependency-aware recovery**
* **Workload reassignment**
* **Digital-twin visualization**
* **Recovery simulation**

The core operational philosophy is:

**Monitor → Understand → Simulate → Recover**

## Key Features

### Command Center

A centralized dashboard providing an operational overview of fleet status, including:

* Online and at-risk units
* Reassigned workloads
* Fleet survival indicators
* Task completion metrics
* Emergency recovery controls

### Fleet Health Monitoring

A dedicated health interface for assessing individual robotic units through parameters such as:

* Battery condition
* Thermal status
* Load levels
* Survival estimates
* Operational risk

### 3D Digital Twin

An interactive visualization of the robotic workspace that represents the fleet within an industrial cell.

Operators can interact with the digital environment, inspect individual units, and understand the spatial relationship between robots and their operating area.

### Failure Propagation

FleetGuard visualizes how the failure of one robot can influence dependent units and downstream operations.

This provides an intuitive representation of **cascading-failure behaviour** and helps operators understand where intervention may be required.

### Recovery Planning

The system presents recovery strategies and operational priorities to support structured decision-making during fleet disruptions.

### Simulation Lab

An interactive simulation environment for exploring different failure conditions and observing their potential effect on fleet performance.

### Manual Work Reassignment

When a robot becomes unavailable, operators can manually determine which healthy unit should inherit the affected workload, providing a **human-in-the-loop recovery mechanism**.

### Emergency Recovery

A dedicated recovery pathway allows operators to respond rapidly to critical fleet conditions rather than relying solely on passive monitoring.

---

## Front-End Implementation

The current version is implemented as a **single-page front-end prototype**, with the interface, styling, and interactive behaviour incorporated directly into the project.

### Technologies

* **HTML5** — interface structure and application layout
* **CSS3** — responsive design, animations, visual hierarchy, and dashboard styling
* **JavaScript** — client-side interactions and simulation behaviour
* **HTML Canvas** — interactive visualizations and fleet-related graphical elements

The prototype incorporates a dark, industrial control-room aesthetic with responsive layouts, animated components, interactive dashboards, visualization panels, and operational status indicators.

## System Concept

FleetGuard is structured around four primary operational stages:

### 01 — Monitor

Continuously observe the health and availability of individual robotic units.

### 02 — Understand

Identify dependencies and determine how a local failure could propagate through the fleet.

### 03 — Simulate

Evaluate potential failure scenarios and recovery conditions before executing an intervention.

### 04 — Recover

Reassign workloads and restore operational continuity through structured recovery actions.

---

## Current Development Status

**Prototype / Front-End Demonstration**

The current implementation focuses specifically on the **user interface and front-end interaction layer**.

It does **not currently include**:

* Production backend infrastructure
* Live robot telemetry
* Physical robot communication
* ROS-based fleet control
* Persistent database integration
* Deployed machine-learning models
* Real-world autonomous task allocation

These components represent potential directions for future development.

## Future Scope

FleetGuard can be further evolved into a complete fleet-recovery platform through integration with:

* **ROS / ROS 2** for robotic communication
* **IoT telemetry** for real-time fleet data
* **Database infrastructure** for historical operational records
* **Machine learning** for predictive failure detection
* **Dependency graphs** for automated cascade analysis
* **Dynamic task allocation** for autonomous workload redistribution
* **Digital-twin synchronization** with physical robotic cells
* **Predictive maintenance** based on historical health patterns
* **Edge and cloud infrastructure** for distributed fleet management

The long-term objective is to transition from a visualization-oriented prototype into an **intelligent, data-driven recovery architecture for autonomous robotic fleets**.

---

## Team

* **Varshini Gadwala** — Systems Lead
* **Vrithika Tada** — Fleet Operations
* **Nithisha Vempalli** — Recovery Engineering

---

## Project Statement

> **Robot Fleet Recovery Under Cascading Failures**

FleetGuard explores how a centralized operational interface can assist human operators in understanding, containing, and recovering from cascading failures within interconnected robotic fleets.

---

### Project Status

**Hackathon Prototype | Front-End Development | Robotics & Autonomous Systems**
