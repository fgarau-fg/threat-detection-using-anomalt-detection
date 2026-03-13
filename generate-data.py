import pandas as pd
import numpy as np
import random


def generate_normal_data(num_samples=10000):
    """genera dati casuali per avere log e per poi analizzarli"""
    data = {
        'login_attempts_per_min': np.random.randint(0, 3, num_samples),
        'files_accessed_per_min': np.random.randint(1, 20, num_samples),
        'cpu_usage_avg': np.random.uniform(5, 40, num_samples),
        'network_out_mb': np.random.uniform(0.1, 5.0, num_samples),
        'process_count': np.random.randint(30, 80, num_samples)
    }
    return pd.DataFrame(data)



def generate_anomalous_data(num_anomalies=200):
    """genera anomalie sintetiche"""
    anomalies = {
        'login_attempts_per_min': np.random.randint(10, 50, num_anomalies),
        'files_accessed_per_min': np.random.randint(50, 200, num_anomalies),
        'cpu_usage_avg': np.random.uniform(80, 100, num_anomalies),
        'network_out_mb': np.random.uniform(50.0, 200.0, num_anomalies),
        'process_count': np.random.randint(100, 200, num_anomalies)
    }
    return pd.DataFrame(anomalies)




if __name__ == '__main__':
        normal_df = generate_normal_data()
        anomalous_df = generate_anomalous_data()

        # shuffle rows
        combined_df = pd.concat([normal_df, anomalous_df], ignore_index=True)
        combined_df = combined_df.sample(frac=1).reset_index(drop=True)


        # save to csv
        combined_df.to_csv("system_activity_logs.csv", index=False)
        print(f"Generated{len(normal_df)} normal samples pyand {len(anomalous_df)} anomalies.")
        print("Data saved to system_activity_logs.csv")
        print("\nFirst 5 rows of generated data:")
        print(combined_df.head())