# Intelligent-Power-Demand-Forecasting
The core objective is to predict electricity demand for every 10-minute block of the day (144 blocks total) for APU, a major power provider. 
This project demonstrates an end-to-end Machine Learning workflow for Electricity Demand Forecasting, including:

✅ Exploratory Data Analysis (EDA), data cleaning, and feature engineering in Jupyter Notebook
✅ Forecasting model (Prophet) with justification
✅ Backend API (FastAPI) for serving forecasts
✅ Frontend Dashboard for visualization
✅ provided data (Utility_consumption.csv)

## 📂 Project Structure


│── Assignment1_Analysis&Modeling.ipynb    # Jupyter Notebook (EDA, cleaning, feature engineering, model justification)  
│
│── Backend/  
│   ├── main.py               # Backend API (FastAPI)  
│   ├── model_meta_v2.json    # Model metadata  
│   ├── prophet_model_v2.pkl  # Trained model  
│   ├── training_data_v2.xlsx # Training dataset  
│
│── Frontend/  
│   ├── index.html            # Main dashboard page  
│   ├── app.js                # JS logic for fetching API data  
│   ├── style.css             # Styling for dashboard 
│
│── Utility_consumption.csv   # Provided data for reproducibility  
│── README.md                 # Project documentation  






