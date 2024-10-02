# E-Commerce Data Dashboard

![Logo](e-commerce_logo.png)

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Data Sources](#data-sources)
- [Author](#author)

## Overview

This project is a data analysis and visualization project focused on public e-commerce data. It includes code for **data wrangling**, **exploratory data analysis (EDA)**, and a **Streamlit dashboard** for interactive data exploration. The goal of this project is to analyze data from the **E-Commerce Public Dataset** and provide meaningful insights through visualizations.

## Project Structure

Here is the structure of the project:

```
E-Commerce Dashboard/
│
├── dashboard.py           # Main script to run the Streamlit application
├── main_data.csv         # Dataset used for analysis
├── e-commerce_logo.png    # Project logo
├── README.md              # This documentation file
└── requirements.txt       # List of required dependencies
```

## Installation

Follow these steps to install and run the application locally:

1. **Clone this repository to your local machine:**

   ```bash
   git clone https://github.com/username/e-commerce-dashboard.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd e-commerce-dashboard
   ```

3. **Install the required Python packages by running:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Data Wrangling

Data wrangling scripts are included in `dashboard.py`, which prepares and cleans the data before analysis.

### Exploratory Data Analysis (EDA)

Explore and analyze the data using the provided Python scripts and visualizations.

### Visualization

Run the Streamlit application for interactive data exploration:

1. **Execute the following command in your terminal:**

   ```bash
   streamlit run dashboard.py
   ```

2. **Access the dashboard in your web browser at:**
   ```
   http://localhost:8501
   ```

## Data Sources

This project utilizes the **E-Commerce Public Dataset** sourced from the final project of the **Data Analysis with Python** course offered by Dicoding.

## Author

**Adriel Fabian Suryoto**  
© 2024 All Rights Reserved
