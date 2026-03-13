import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns


# costanti

DATA_FILE = 'C:\\Users\\FedericoGarau\\OneDrive - Nethica Srl\\Desktop\\Vari\\Appprendimento\\Python Projects\\threat-detection-using-anomaly-detection\\system_activity_logs.csv'
MODEL_PATH = "isolation_forest_model.pkl"
CONTAMINATION_RATE=0.02


df = pd.read_csv(DATA_FILE)



def train_model(df, contamination=CONTAMINATION_RATE):
    print("Training isolation forest model...")
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(df)
    print("Model training complete")
    return model 


def predict_anomalies(model, df):
    """predice le anomalie usando il modello precedentemente allenato"""
    print("Predicting anomalies...")
    # creo una copia del df perche devo aggiungerci colonne
    df_with_predictions = df.copy()

    # il modello restituisce -1 per le anomalie e 1 per le normali
    df_with_predictions['anomaly_score'] = model.decision_function(df)
    df_with_predictions['is_anomaly'] = model.predict(df)

    return df_with_predictions





def visualize_results(df): 
    print("Generating visualizations...")

    plt.figure(figsize=(16, 6))

    # Scatter plot of two features, colored by anomaly status
    plt.subplot(1, 2, 1)
    sns.scatterplot(
        x='cpu_usage_avg',
        y='network_out_mb',
        hue='is_anomaly',
        palette={1: 'green', -1: 'red'},
        data=df, s=100, alpha=0.7)
    plt.title('CPU Usage vs. Network Out(Anomalies in Red)')
    plt.xlabel('Average CPU Usage (%)')
    plt.ylabel('Network Out (MB)')

    # Distribution of Anomaly Scores
    plt.subplot(1, 2, 2)
    sns.histplot(df['anomaly_score'], kde=True, bins=50)
    plt.axvline(
        x=df[df['is_anomaly'] == -1]['anomaly_score'].max(),
        color='red',
        linestyle='--',
    label='Anomaly Threshold')
    plt.title('Distribution of Anomaly Scores')
    plt.xlabel('Anomaly Score')
    plt.ylabel('Count')
    plt.legend()

    plt.tight_layout()
    plt.show()


def main():
    # 1. Load Data
    try:
        df = pd.read_csv(DATA_FILE)
        print(f"Loaded data from {DATA_FILE}.Shape: {df.shape}")
    except FileNotFoundError:
        print(f"Error: {DATA_FILE} not found.")
        return

    # 2. Train Model
    model = train_model(df)

    # 3. Predict Anomalies
    # Pass the original DataFrame here
    df_results = predict_anomalies(model, df)

    # 4. Display Anomalies
    anomalies = df_results[df_results['is_anomaly'] == -1]
    normal_data = df_results[df_results['is_anomaly'] == 1]

    print(f"\nFound {len(anomalies)} anomalies and {len(normal_data)} normal data points.")
    if not anomalies.empty :
        print("\n--- Detected Anomalies ---")

        # Show top 5 most anomalous
        print(anomalies.sort_values(by='anomaly_score').head())

        # here you can implement an alerting mechanism
        # for _, row in anomalies.iterrows():send_alert(..)

    else:
        print("\nNo anomalies detected.")

    # 5. Visualize Results
    visualize_results(df_results)


if __name__ == "__main__":
    main()  