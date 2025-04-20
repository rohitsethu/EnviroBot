import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

st.set_page_config(page_title="AI Air Pollution Predictor", layout="centered")

st.title("Air Pollution Level Predictor")
st.markdown("Predict AQI (Air Quality Index) based on temperature, traffic, and industrial activity using a machine learning model.")

np.random.seed(42)
temperature = np.random.randint(15, 45, 200)
traffic = np.random.randint(1, 11, 200)
industry = np.random.randint(1, 11, 200)
aqi = 0.5 * temperature + 5 * traffic + 4 * industry + np.random.normal(0, 10, 200)

data = pd.DataFrame({
    "Temperature (°C)": temperature,
    "Traffic Level": traffic,
    "Industrial Activity": industry,
    "Air Quality Index": aqi
})

X = data[["Temperature (°C)", "Traffic Level", "Industrial Activity"]]
y = data["Air Quality Index"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

st.sidebar.header("Input Parameters")
input_temp = st.sidebar.slider("🌡️ Temperature (°C)", 10, 50, 30)
input_traffic = st.sidebar.slider("🚗 Traffic Level (1-10)", 1, 10, 5)
input_industry = st.sidebar.slider("🏭 Industrial Activity (1-10)", 1, 10, 5)

input_data = np.array([[input_temp, input_traffic, input_industry]])
predicted_aqi = model.predict(input_data)[0]

st.subheader("Predicted Air Quality Index")
st.success(f" **{predicted_aqi:.2f} AQI** (based on your inputs)")

st.subheader("Actual vs Predicted (Test Set)")
fig, ax = plt.subplots()
ax.scatter(y_test, y_pred, alpha=0.6, color='green')
ax.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], 'r--')
ax.set_xlabel("Actual AQI")
ax.set_ylabel("Predicted AQI")
st.pyplot(fig)

st.markdown("### Model Performance")
st.write(f"**R² Score:** {r2:.2f}")
st.write(f"**Mean Squared Error:** {mse:.2f}")
