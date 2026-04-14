print("code started ...")
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Load dataset
data = pd.read_csv('data/energy_4 days.csv', encoding='latin1', parse_dates=['Datetime'], index_col='Datetime')

# Resample hourly
data = data.resample('h').mean()

# Fill missing values
data = data.ffill()

# Feature Engineering
data['hour'] = data.index.hour
data['day'] = data.index.dayofweek

# Features and target
X = data[['hour', 'day']]
y = data['Energy']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# scalling
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Model
model = MLPRegressor(hidden_layer_sizes=(64,64), max_iter=500, random_state=42)
model.fit(X_train, y_train)

# Prediction
pred = model.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, pred )
rmse = mse ** 0.5

print("✅ RMSE:", rmse)

# Save model
joblib.dump(model, 'models/model.pkl')

# Visualization
plt.figure(figsize=(10,5))
plt.plot(y_test.values[:50], label='Actual')
plt.plot(pred[:50], label='Predicted')
plt.legend()
plt.title("Energy Forecasting")
plt.savefig('images/prediction.png')
plt.show()
input("Press Enter to exit ...")