import datetime
import json
from collections import defaultdict
import math
import csv

# Frequency-Based Behavioral Attack

def freq_behavior_attack(original_file, anonymized_file, output_file):
    def preprocess(file_path):
        """Preprocess the dataset to extract location frequency and temporal behavior."""
        data = defaultdict(lambda: defaultdict(lambda: {"locations": defaultdict(int), "activity": defaultdict(int)}))

        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter="\t")
            for row in reader:
                if row[0] != "DEL":
                    id = row[0]
                    timestamp = datetime.datetime.fromisoformat(row[1])
                    year_week = f"{timestamp.year}-{timestamp.isocalendar()[1]}"
                    lat, lon = round(float(row[2]), 4), round(float(row[3]), 4)
                    hour = timestamp.hour

                    # Record location frequency
                    data[id][year_week]["locations"][(lat, lon)] += 1

                    # Record hourly activity
                    data[id][year_week]["activity"][hour] += 1

        return data

    def calculate_similarity(original_behavior, anonymized_behavior):
        """Calculate similarity between original and anonymized behaviors."""
        similarity_score = 0

        # Compare location frequencies
        for location, orig_count in original_behavior["locations"].items():
            anon_count = anonymized_behavior["locations"].get(location, 0)
            similarity_score += min(orig_count, anon_count)

        # Compare hourly activity patterns
        for hour, orig_count in original_behavior["activity"].items():
            anon_count = anonymized_behavior["activity"].get(hour, 0)
            similarity_score += min(orig_count, anon_count)

        return similarity_score

    def match_ids(original_data, anonymized_data):
        """Match original IDs to anonymized IDs based on behavioral similarity."""
        results = defaultdict(lambda: defaultdict(list))

        for orig_id, orig_weeks in original_data.items():
            for week, orig_behavior in orig_weeks.items():
                max_similarity = -1
                best_match = None

                for anon_id, anon_weeks in anonymized_data.items():
                    if week in anon_weeks:
                        anon_behavior = anon_weeks[week]
                        similarity = calculate_similarity(orig_behavior, anon_behavior)

                        if similarity > max_similarity:
                            max_similarity = similarity
                            best_match = anon_id

                if best_match:
                    results[orig_id][week].append(best_match)

        return results

    # Step 1: Preprocess both datasets
    original_data = preprocess(original_file)
    anonymized_data = preprocess(anonymized_file)

    # Step 2: Match IDs
    matched_ids = match_ids(original_data, anonymized_data)

    # Step 3: Write results to output file
    with open(output_file, 'w') as f:
        json.dump(matched_ids, f, indent=4)

# Example usage
if __name__ == "__main__":
    original_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_origin/big_survey_results.csv" 
    anonymized_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_ano/Laplace_anonymized_big_survey_results.csv"   
    output_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/attack_phase/output/freq_behavior_big_survey_attack.json"

    # Run the frequency-based behavioral attack
    freq_behavior_attack(original_file, anonymized_file, output_file)
