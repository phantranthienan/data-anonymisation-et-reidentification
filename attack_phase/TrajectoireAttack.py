import datetime
from collections import defaultdict
import json
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw  # Dynamic Time Warping library
from sklearn.cluster import DBSCAN
import numpy as np

# Improved Trajectory-Based Attack with Temporal Matching and Weighted Analysis
def trajectoire_attack(original_data, anonymized_data, output_file):
    def preprocess(data):
        """Preprocess the dataset to extract trajectory and temporal information."""
        result = defaultdict(lambda: defaultdict(list))
        temporal_patterns = defaultdict(lambda: defaultdict(dict))

        for _, row in data.iterrows():
            ID = row[0]
            timestamp = datetime.datetime.fromisoformat(row[1])
            year_week = f"{timestamp.year}-{timestamp.isocalendar()[1]}"
            lat, lon = round(row[2], 4), round(row[3], 4)

            # Store trajectory data
            result[ID][year_week].append((timestamp, (lat, lon)))

            # Store temporal patterns
            hour = timestamp.hour
            if "hourly_count" not in temporal_patterns[ID][year_week]:
                temporal_patterns[ID][year_week]["hourly_count"] = defaultdict(int)
            temporal_patterns[ID][year_week]["hourly_count"][hour] += 1

        return result, temporal_patterns

    def calculate_trajectory_similarity(orig_traj, anon_traj):
        """Calculate similarity between two trajectories using Dynamic Time Warping (DTW)."""
        orig_points = [point[1] for point in orig_traj]  # Extract coordinates
        anon_points = [point[1] for point in anon_traj]
        distance, _ = fastdtw(orig_points, anon_points, dist=euclidean)
        return 1 / (1 + distance)  # Convert distance to similarity score

    def calculate_temporal_similarity(orig_temporal, anon_temporal):
        """Calculate similarity between temporal activity patterns."""
        score = 0
        total_hours = 0
        for hour in range(24):
            orig_count = orig_temporal.get(hour, 0)
            anon_count = anon_temporal.get(hour, 0)
            score += min(orig_count, anon_count)  # Overlap of activity
            total_hours += max(orig_count, anon_count)
        return score / total_hours if total_hours > 0 else 0

    def cluster_locations(locations):
        """Cluster GPS points to find significant locations using DBSCAN."""
        coords = np.array([loc[1] for loc in locations])
        clustering = DBSCAN(eps=0.001, min_samples=2).fit(coords)
        clusters = defaultdict(list)
        for idx, label in enumerate(clustering.labels_):
            clusters[label].append(coords[idx])
        return clusters

    # Preprocess original and anonymized datasets
    original_features, original_temporal = preprocess(original_data)
    anonymized_features, anonymized_temporal = preprocess(anonymized_data)

    # Perform matching
    results = defaultdict(lambda: defaultdict(list))
    for orig_id, weeks in original_features.items():
        for week, orig_traj in weeks.items():
            max_similarity = -1
            best_match = None

            orig_clusters = cluster_locations(orig_traj)
            orig_temporal_pattern = original_temporal[orig_id][week]["hourly_count"]

            for anon_id, anon_weeks in anonymized_features.items():
                if week in anon_weeks:
                    anon_traj = anonymized_features[anon_id][week]
                    anon_clusters = cluster_locations(anon_traj)
                    anon_temporal_pattern = anonymized_temporal[anon_id][week]["hourly_count"]

                    # Calculate similarities
                    trajectory_similarity = calculate_trajectory_similarity(orig_traj, anon_traj)
                    temporal_similarity = calculate_temporal_similarity(orig_temporal_pattern, anon_temporal_pattern)

                    # Weighted similarity score
                    overall_similarity = 0.5 * trajectory_similarity + 0.3 * temporal_similarity

                    if overall_similarity > max_similarity:
                        max_similarity = overall_similarity
                        best_match = anon_id

            # Save the best match for this original ID and week
            if best_match:
                results[orig_id][week].append(best_match)

    # Write the results to the output JSON file
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)

# Example usage
if __name__ == "__main__":
    import pandas as pd
    # original_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_origin/survey_results_1.csv"  
    # anonymized_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_ano/ano_1.csv"   
    # output_json = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/attack_phase/output/trajectoire_attack_data_1.json" 


    # original_data = pd.read_csv(original_file, sep="\t")  # Adjust separator if needed
    # anonymized_data = pd.read_csv(anonymized_file, sep="\t")

    # # Run the attack
    # trajectoire_attack(original_data, anonymized_data, output_json)

    # original_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_origin/survey_results_2.csv"  
    # anonymized_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_ano/ano_2.csv"   
    # output_json = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/attack_phase/output/trajectoire_attack_data_2.json" 


    # original_data = pd.read_csv(original_file, sep="\t")  # Adjust separator if needed
    # anonymized_data = pd.read_csv(anonymized_file, sep="\t")

    # # Run the attack
    # trajectoire_attack(original_data, anonymized_data, output_json)

    # original_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_origin/survey_results_3.csv"  
    # anonymized_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_ano/ano_3.csv"   
    # output_json = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/attack_phase/output/trajectoire_attack_data_3.json" 


    # original_data = pd.read_csv(original_file, sep="\t")  # Adjust separator if needed
    # anonymized_data = pd.read_csv(anonymized_file, sep="\t")

    # # Run the attack
    # trajectoire_attack(original_data, anonymized_data, output_json)
    
########################################################################################################################
        
    original_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_origin/survey_results.csv"  
    anonymized_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_ano/anonymized_survey_data.csv"   
    output_json = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/attack_phase/output/trajectoire_attack_survey_data.json" 

    original_data = pd.read_csv(original_file, sep="\t")  # Adjust separator if needed
    anonymized_data = pd.read_csv(anonymized_file, sep="\t")

    # Run the attack
    trajectoire_attack(original_data, anonymized_data, output_json)

    original_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_origin/big_survey_results.csv"  
    anonymized_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_ano/anonymized_big_survey_data.csv"   
    output_json = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/attack_phase/output/trajectoire_attack_big_survey_data.json" 

    original_data = pd.read_csv(original_file, sep="\t")  # Adjust separator if needed
    anonymized_data = pd.read_csv(anonymized_file, sep="\t")

    # Run the attack
    trajectoire_attack(original_data, anonymized_data, output_json)

    original_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_origin/bigger_survey_results.csv"  
    anonymized_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_ano/anonymized_bigger_survey_data.csv"   
    output_json = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/attack_phase/output/trajectoire_attack_bigger_survey_data.json" 

    original_data = pd.read_csv(original_file, sep="\t")  # Adjust separator if needed
    anonymized_data = pd.read_csv(anonymized_file, sep="\t")

    # Run the attack
    trajectoire_attack(original_data, anonymized_data, output_json)


