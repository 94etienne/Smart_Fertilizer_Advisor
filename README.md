# 🌱 Fertilizer Recommendation System

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A machine learning-powered web application that recommends optimal fertilizers and application rates based on soil parameters.

![Dashboard Screenshot](screenshot.png)

## Features

- **Precision Recommendations**: Predicts fertilizer type and quantity (kg/ha)
- **Responsive Dashboard**: Works on desktop, tablet, and mobile
- **Soil Parameter Analysis**: Accepts 7 critical soil metrics
- **Visual Analytics**: Interactive feature importance charts
- **Model Transparency**: Displays key decision factors

## Model Architecture

```mermaid
graph TD
    A[Soil Parameters] --> B(Preprocessing)
    B --> C[Classification Model]
    B --> D[Regression Model]
    C --> E[Fertilizer Type]
    D --> F[Application Rate]
    E --> G[Recommendation Dashboard]
    F --> G