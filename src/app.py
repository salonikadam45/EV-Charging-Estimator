import os
import streamlit as st
import pandas as pd
import joblib

# Load the saved model and columns reliably
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'ev_model.pkl')
columns_path = os.path.join(BASE_DIR, 'model_columns.pkl')

model = joblib.load(model_path)
model_columns = joblib.load(columns_path)

st.set_page_config(page_title="EV Charging Energy Estimator", page_icon="⚡", layout="centered")

st.title("⚡ EV Charging Energy & Duration Estimator")
st.write("Predict the energy consumption ($\\text{kWh}$) of an electric vehicle charging session using machine learning.")

st.sidebar.header("🔌 Session Parameters")

# Sidebar input widgets corresponding to your dataset features
battery_capacity = st.sidebar.number_input("Battery Capacity (kWh)", min_value=10.0, max_value=150.0, value=75.0, step=1.0)
charging_rate = st.sidebar.number_input("Charging Rate (kW)", min_value=2.0, max_value=350.0, value=50.0, step=1.0)
charging_cost = st.sidebar.number_input("Charging Cost (USD)", min_value=0.0, max_value=100.0, value=15.0, step=0.5)
start_soc = st.sidebar.slider("Start State of Charge (Start %)", min_value=0, max_value=99, value=20, step=1)
end_soc = st.sidebar.slider("End State of Charge (End %)", min_value=1, max_value=100, value=80, step=1)
distance_driven = st.sidebar.number_input("Distance Driven since last charge (km)", min_value=0.0, max_value=1000.0, value=150.0, step=10.0)
temperature = st.sidebar.number_input("Ambient Temperature (°C)", min_value=-30.0, max_value=50.0, value=25.0, step=1.0)
vehicle_age = st.sidebar.number_input("Vehicle Age (years)", min_value=0, max_value=20, value=3, step=1)

# Calculate engineered feature dynamically
soc_difference = end_soc - start_soc

# Validation check
if start_soc >= end_soc:
    st.sidebar.warning("⚠️ End SoC should be greater than Start SoC.")

# Main Panel Prediction Button
if st.button("Predict Energy Consumption", type="primary"):
    # Create a dictionary matching the training features
    input_data = {
        'Battery Capacity (kWh)': [battery_capacity],
        'Charging Rate (kW)': [charging_rate],
        'Charging Cost (USD)': [charging_cost],
        'State of Charge (Start %)': [start_soc],
        'State of Charge (End %)': [end_soc],
        'Distance Driven (since last charge) (km)': [distance_driven],
        'Temperature (°C)': [temperature],
        'Vehicle Age (years)': [vehicle_age],
        'SoC_Difference': [soc_difference]
    }
    
    input_df = pd.DataFrame(input_data)
    
    # Ensure columns align with what the model expects
    input_df = input_df.reindex(columns=model_columns, fill_value=0)
    
    # Predict using the loaded model
    prediction = model.predict(input_df)[0]
    
    st.success(f"### Predicted Energy Consumed: **{prediction:.2f} kWh**")
    st.info(f"Summary: Charging your EV from {start_soc}% to {end_soc}% will require approximately {prediction:.2f} kWh of electrical energy.")
