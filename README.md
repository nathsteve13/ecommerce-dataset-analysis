# E-Commerce Data Analysis

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Data Sources](#data-sources)
- [Project Summary](#project-summary)

## Overview
Welcome to the **E-Commerce Data Analysis** project! This project explores e-commerce data to uncover trends, patterns, and insights into customer behaviors and sales performance. Using publicly available Brazilian E-Commerce datasets, this analysis provides a comprehensive view of how e-commerce operates in various regions across Brazil.

## Project Structure
- `dashboard/`: Contains the `dashboard.py` file, which generates the Streamlit dashboard for visualizing the analysis results.
- `data/`: Directory containing raw CSV data files including customer, product, order, payment, and review data.
  - `customers_dataset.csv`: Contains customer information including city and state.
  - `geolocation_dataset.csv`: Contains geolocation information for customer orders.
  - `order_items_dataset.csv`: Provides details about the items in each order.
  - `order_payments_dataset.csv`: Includes payment method and transaction details.
  - `order_reviews_dataset.csv`: Holds customer reviews and ratings for orders.
  - `orders_dataset.csv`: Contains metadata about the orders, such as timestamps and status.
  - `product_category_name_translation.csv`: Translates product category names into English.
  - `products_dataset.csv`: Information about products available in the dataset.
  - `sellers_dataset.csv`: Contains information about sellers and their locations.
- `notebook.ipynb`: Jupyter Notebook used for data exploration and analysis.
- `README.md`: Project documentation (this file).
- `requirements.txt`: Lists all necessary Python libraries for the project.
- `url.txt`: A text file storing URLs, potentially for external references.

## Installation
To set up and run this project locally:

1. Clone this repository:
   ```bash
   git clone https://github.com/nathsteve13/ecommerce-dataset-analysis.git
   ```

2. Navigate to the project directory:
   ```bash
   cd ecommerce-dataset-analysis
   ```

3. Install the required Python libraries by running:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. **Data Wrangling and Exploration**: Use `notebook.ipynb` for preparing and cleaning the data. This Jupyter Notebook covers data wrangling, EDA (Exploratory Data Analysis), and visualization.

2. **Interactive Dashboard**: Visualize key metrics and trends by launching the Streamlit dashboard:
   ```bash
   cd dashboard
   streamlit run dashboard.py
   ```
   Once launched, you can interact with the dashboard through `http://localhost:8501` in your browser.

## Data Sources
This project uses the **Brazilian E-Commerce Public Dataset**, available on [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

For a live version of the dashboard, visit [Dashboard](https://nathsteve13-ecommerce-dataset-analysi-dashboarddashboard-yulnre.streamlit.app/).

## Project Summary

This project delivers in-depth analysis and insights into Brazil's e-commerce market by analyzing various data points such as orders, payments, products, and customer reviews. Below are some of the significant conclusions drawn from the analysis:

### 1. **Most Frequently Used Payment Method**:
   - **Credit cards** are the most commonly used payment method, surpassing other options like boleto, debit cards, and vouchers. This preference is likely due to the convenience and wide acceptance of credit cards in Brazil.

### 2. **Top and Lowest Revenue-Generating Product Categories**:
   - The **lowest revenue** comes from the *seguros_e_servicos* (insurance and services) category, generating only 283.29 in total revenue, suggesting lower demand for non-physical products.
   - In contrast, the **highest revenue** is from the *beleza_saude* (beauty and health) category, with a total revenue of 1,258,681.34, indicating a strong demand for beauty and health-related products.

### 3. **Top-Selling Products by Region**:
   - The *beleza_saude* (Beauty and Health) category dominates in several regions, including Alagoas (AL), Amazonas (AM), and Bahia (BA), showcasing its nationwide popularity.
   - *Cama_mesa_banho* (Bedding, Bath, and Home) products are highly demanded in São Paulo (SP), Rio de Janeiro (RJ), and Minas Gerais (MG), highlighting regional preferences for home-related products.
   - In some regions, such as Mato Grosso do Sul (MS) and Santa Catarina (SC), *esporte_lazer* (Sports and Leisure) stands out, indicating local interest in sports and leisure activities.

### 4. **Average Delivery Times Across Regions**:
   - Urbanized areas like São Paulo (SP) enjoy the fastest delivery times, with an average of 8.64 days, while remote areas such as Roraima (RR) face the longest delivery times at 31.32 days.
   - These differences underline the logistical challenges present in Brazil's more remote regions, emphasizing the need for better infrastructure in these areas.

### 5. **Monthly Revenue Trends**:
   - The data shows revenue peaks in November and December 2017, likely corresponding to Black Friday and holiday shopping seasons. November 2017 saw the highest revenue, reaching 994,849.49.
   - A sudden drop in revenue in September 2018 (145.00) could indicate incomplete data or an anomaly in the dataset.

### 6. **Customer Geographical Distribution**:
   - The majority of orders are concentrated in the southeast region of Brazil, especially in São Paulo, Rio de Janeiro, and Minas Gerais. This concentration reflects high e-commerce activity in these economically significant states.
   - The northeast and southern regions also show activity but to a lesser extent.
   - Northern and central Brazil show limited activity, suggesting potential areas for market growth.


---

**Name:** Nathanael Steven Soetrisno  
**Data Source:** [Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

--- 
