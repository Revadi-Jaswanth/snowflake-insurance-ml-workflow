# snowflake-insurance-ml-workflow

# End-to-End Insurance Cost Prediction ML Workflow Using Snowflake

## Overview

This project implements an end-to-end machine learning workflow in Snowflake for predicting medical insurance charges.

The project uses an XGBoost regression model and demonstrates data preparation, model training, evaluation, model registration, warehouse inference, automated prediction using Snowflake Streams and Tasks, and a Streamlit application for interactive predictions.

## Machine Learning Problem

Regression

The objective is to predict insurance charges based on customer information.

## Dataset

Medical Cost Personal Dataset

Features:

- Age
- Sex
- BMI
- Children
- Smoker
- Region

Target:

- Charges

Dataset size: 1,338 records.

## Machine Learning Model

XGBoost Regressor

### Evaluation Results

- MAE: 2818.00
- RMSE: 5057.39
- R²: 0.8261

## Snowflake Architecture

```text
Insurance Dataset
        |
        v
Data Preparation
        |
        v
Train/Test Split
        |
        v
XGBoost Regression
        |
        v
Model Evaluation
        |
        v
Snowflake Model Registry
        |
        v
INSURANCE_CHARGES_MODEL V2
        |
        +----------------------+
        |                      |
        v                      v
Incoming Data             Streamlit App
        |                      |
        v                      v
Snowflake Stream       Model V2 Inference
        |
        v
Triggered Task
        |
        v
Stored Procedure
        |
        v
Model Inference
        |
        v
INSURANCE_PREDICTIONS
