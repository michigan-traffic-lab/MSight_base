# 🚗 MSight Base: Base library for MSight System

This library serves as the foundational module for the MSight Perception system, providing essential tools and utilities for processing, analyzing, and visualizing road object trajectories and related data. It includes core functionalities such as trajectory modeling, road object representation, behavior analysis, and visualization utilities, enabling seamless integration with higher-level perception and decision-making systems.

The library is designed to support autonomous vehicle research and development by offering reusable components that simplify working with spatial and temporal data in real-world traffic scenarios.

## 📈 Trajectory Manager

The Trajectory Manager is a core component of the MSight Base library, designed to handle the modeling, storage, and manipulation of road object trajectories. It provides a robust framework for working with spatial and temporal data, enabling efficient trajectory analysis and visualization.

The Trajectory Manager simplifies the process of managing road object trajectories by offering **Trajectory Modeling** that define and represent object trajectories with fast retrieval of their spatial and temporal attributes, along with advanced querying capabilities for frame-based analysis.

## 🎨 Visualization

The Visualization module in the MSight Base library provides tools to create graphical representations of road object trajectories and related spatial data. It is designed to help developers and researchers analyze and debug trajectory data effectively using interactive basemap rendering and real-time trajectory visualization.

## 🐳 Docker

To run MSight Base in a containerized environment:

```bash
docker build -t msight_base .
docker run -it msight_base
```

## 🛠️ Developers

- Rusheng Zhang (rushengz@umich.edu)

## 📧 Contact

- Henry Liu (henryliu@umich.edu)
