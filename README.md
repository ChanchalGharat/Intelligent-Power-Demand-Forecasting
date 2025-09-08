## Intelligent-Power-Demand-Forecasting
The core objective is to predict electricity demand for every 10-minute block of the day (144 blocks total) for APU, a major power provider. 
This project demonstrates an end-to-end Machine Learning workflow for Electricity Demand Forecasting, including:

✅ Exploratory Data Analysis (EDA), data cleaning, and feature engineering in Jupyter Notebook

✅ Forecasting model (Prophet) with justification

✅ Backend API (FastAPI) for serving forecasts

✅ Frontend Dashboard for visualization

✅ provided data (Utility_consumption.csv)

## 📂 Project Structure

│── Assignment1_Analysis&Modeling.ipynb # Jupyter Notebook (EDA, cleaning, feature engineering, model justification)
│
│── Backend/  
│   ├── main.py               # Backend API (FastAPI/Flask)  
│   ├── model_meta_v2.json    # Model metadata  
│   ├── prophet_model_v2.pkl  # Trained model  
│   ├── training_data_v2.xlsx # Training dataset 
│   ├── requirement.txt       # Python dependencies
│
│── Frontend/  
│   ├── index.html            # Main dashboard page  
│   ├── app.js                # JS logic for fetching API data  
│   ├── style.css             # Styling for dashboard
│── Utility_consumption.csv   # Provided data for reproducibility  
│── README.md                 # Project documentation  

## Install dependencies 
pip install -r backend/requirements.txt

## Open backend folder in vs code 
run below code in terminal 
uvicorn main:app --reload

## Open frontend folder in vs code 
right click on index.html and Open with Live Server

## You will see the web page like this -
<img width="1355" height="681" alt="image" src="https://github.com/user-attachments/assets/50586fea-dfa8-46f8-8cbf-679816f0c681" />




