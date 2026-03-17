import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from sklearn.ensemble import IsolationForest

# 1. Data Ingestion Module (As described in Exhibit B)
def ingest_hospital_data(raw_payload: str):
    """
    Simulates the ingestion of hospital reports in JSON format.
    """
    data = json.loads(raw_payload)
    return {
        "zip_code": data.get("zip_code"),
        "temperature": float(data.get("temp", 0)),
        "cluster_density": float(data.get("density", 0))
    }

# 2. Dataset Generation for Prototype
np.random.seed(42)
# Simulate normal seasonal health patterns (Baseline)
normal_data = pd.DataFrame({
    'temperature': np.random.normal(99.0, 0.7, 190),
    'cluster_density': np.random.normal(3, 1.2, 190)
})
# Simulate outbreak signals (Anomalies)
outbreak_data = pd.DataFrame({
    'temperature': np.random.normal(102.8, 1.0, 10),
    'cluster_density': np.random.normal(18, 2.5, 10)
})
df = pd.concat([normal_data, outbreak_data]).sample(frac=1).reset_index(drop=True)

# 3. Machine Learning Model (Anomaly Detection)
# Configuration consistent with Exhibit B: contamination=0.05
model = IsolationForest(contamination=0.05, random_state=42)
df['is_anomaly'] = model.fit_predict(df[['temperature', 'cluster_density']])

# 4. Visualization of Results (Figure B1)
plt.figure(figsize=(10,6))
for label, color in [(1, "blue"), (-1, "red")]:
    subset = df[df['is_anomaly'] == label]
    plt.scatter(subset['temperature'], subset['cluster_density'], 
                label=("Normal" if label==1 else "Anomaly"), alpha=0.7)

plt.xlabel("Temperature (°F)")
plt.ylabel("Cluster Density")
plt.title("Epidemiological Anomaly Detection - Prototype B1")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig("outputs/figure_B1.png", dpi=300)
print("Pipeline executed: Anomaly detection results saved in outputs/figure_B1.png")
