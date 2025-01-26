import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Load original dataset
original_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_origin/big_survey_results.csv"  # Path to your original file
anonymized_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_ano/combined_anonymized_big_survey_results.csv"  # Output anonymized file
# Parameters
epsilon = 0.5  # Privacy budget for Differential Privacy
gps_noise_scale = 0.001  # Noise scale for GPS coordinates (e.g., ± neighborhood)
date_noise_days = 2  # Max days of noise for timestamps
k = 3  # k for k-Anonymity

# Load the data
df = pd.read_csv(original_file)

# Function to add Laplace noise for Differential Privacy
def add_laplace_noise(value, scale):
    return value + np.random.laplace(0, scale)

# Anonymize GPS coordinates with Differential Privacy
def anonymize_gps(data, scale):
    data["latitude"] = data["latitude"].apply(lambda x: round(add_laplace_noise(x, scale), 3))
    data["longitude"] = data["longitude"].apply(lambda x: round(add_laplace_noise(x, scale), 3))
    return data

# Anonymize timestamps (randomized within the same week)
def anonymize_dates(data, max_days):
    def randomize_within_week(date_str):
        date = datetime.strptime(date_str, "%Y-%m-%d")
        noise = np.random.randint(-max_days, max_days + 1)
        randomized_date = date + timedelta(days=noise)
        # Ensure within the same week
        if randomized_date.isocalendar()[1] != date.isocalendar()[1]:
            return date_str
        return randomized_date.strftime("%Y-%m-%d")
    
    data["timestamp"] = data["timestamp"].apply(randomize_within_week)
    return data

# Group data for k-Anonymity
def apply_k_anonymity(data, k):
    data["region"] = data["latitude"].round(1).astype(str) + "," + data["longitude"].round(1).astype(str)
    grouped = data.groupby("region").filter(lambda x: len(x) >= k)
    return grouped

# Identify POIs and aggregate
def aggregate_poi(data):
    data["period"] = data["timestamp"].apply(lambda x: categorize_time(x))
    grouped_poi = data.groupby(["user_id", "period", "region"]).size().reset_index(name="visits")
    return grouped_poi

def categorize_time(timestamp):
    hour = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").hour
    if 22 <= hour or hour < 6:
        return "Night"
    elif 9 <= hour < 16:
        return "Work"
    elif 10 <= hour < 18:
        return "Weekend"
    return "Other"

# Anonymization pipeline
def anonymize_data(original_file, epsilon, gps_scale, date_noise, k):
    df = pd.read_csv(original_file)
    # Differential Privacy for GPS
    df = anonymize_gps(df, gps_scale)
    # Differential Privacy for Dates
    df = anonymize_dates(df, date_noise)
    # Apply k-Anonymity
    df = apply_k_anonymity(df, k)
    # Aggregate POI
    poi_data = aggregate_poi(df)
    # Save anonymized data
    df.to_csv(anonymized_file, index=False)
    return df, poi_data

# Run anonymization
anonymized_df, poi_data = anonymize_data(original_file, epsilon, gps_noise_scale, date_noise_days, k)

# Save results
anonymized_df.to_csv("anonymized_survey.csv", index=False)
poi_data.to_csv("poi_summary.csv", index=False)
print("Anonymization complete. Anonymized data saved.")
