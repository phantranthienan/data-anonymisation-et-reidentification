import datetime
import json
from collections import defaultdict
import csv


def combined_attack(original_file, anonymized_file, output_file):
    def preprocess_files(file_path):
        """Preprocess the dataset to extract relevant features for comparison."""
        features = defaultdict(lambda: defaultdict(dict))

        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter="\t")
            for row in reader:
                if row[0] != "DEL":
                    id = row[0]
                    timestamp = datetime.datetime.fromisoformat(row[1])
                    year_week = f"{timestamp.year}-{timestamp.isocalendar()[1]}"
                    lat, lon = float(row[2]), float(row[3])

                    if "sum_lat" not in features[id][year_week]:
                        features[id][year_week]["sum_lat"] = 0
                        features[id][year_week]["sum_lon"] = 0
                        features[id][year_week]["count"] = 0

                    features[id][year_week]["sum_lat"] += lat
                    features[id][year_week]["sum_lon"] += lon
                    features[id][year_week]["count"] += 1

        return features

    def calculate_average(features):
        """Calculate averages for GPS coordinates."""
        averages = {}
        for id, weeks in features.items():
            averages[id] = {}
            for week, data in weeks.items():
                avg_lat = data["sum_lat"] / data["count"]
                avg_lon = data["sum_lon"] / data["count"]
                averages[id][week] = (avg_lat, avg_lon)
        return averages

    def calculate_temporal_similarity(orig_weekly_counts, anon_weekly_counts):
        """Calculate temporal similarity based on hourly activity patterns."""
        score = 0
        total_hours = 0
        for hour in range(24):
            orig_count = orig_weekly_counts.get(hour, 0)
            anon_count = anon_weekly_counts.get(hour, 0)
            score += min(orig_count, anon_count)
            total_hours += max(orig_count, anon_count)
        return score / total_hours if total_hours > 0 else 0

    def match_ids(original_avg, anonymized_avg, original_temporal, anonymized_temporal):
        """Match original IDs to anonymized IDs based on combined similarity metrics."""
        results = defaultdict(lambda: defaultdict(list))

        for orig_id, orig_weeks in original_avg.items():
            for week, orig_coords in orig_weeks.items():
                max_similarity = -1
                best_match = None

                for anon_id, anon_weeks in anonymized_avg.items():
                    if week in anon_weeks:
                        anon_coords = anon_weeks[week]

                        # Calculate spatial similarity
                        spatial_similarity = 1 / (1 + abs(orig_coords[0] - anon_coords[0]) + abs(orig_coords[1] - anon_coords[1]))

                        # Calculate temporal similarity
                        orig_temporal_pattern = original_temporal[orig_id].get(week, defaultdict(int))
                        anon_temporal_pattern = anonymized_temporal[anon_id].get(week, defaultdict(int))
                        temporal_similarity = calculate_temporal_similarity(orig_temporal_pattern, anon_temporal_pattern)

                        # Combined similarity score
                        combined_similarity = 0.7 * spatial_similarity + 0.3 * temporal_similarity

                        if combined_similarity > max_similarity:
                            max_similarity = combined_similarity
                            best_match = anon_id

                if best_match:
                    results[orig_id][week].append(best_match)

        return results

    def extract_temporal_patterns(file_path):
        """Extract hourly activity patterns for temporal similarity."""
        temporal_patterns = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter="\t")
            for row in reader:
                if row[0] != "DEL":
                    id = row[0]
                    timestamp = datetime.datetime.fromisoformat(row[1])
                    year_week = f"{timestamp.year}-{timestamp.isocalendar()[1]}"
                    hour = timestamp.hour
                    temporal_patterns[id][year_week][hour] += 1

        return temporal_patterns

    # Step 1: Preprocess original and anonymized files
    original_features = preprocess_files(original_file)
    anonymized_features = preprocess_files(anonymized_file)

    # Step 2: Extract temporal activity patterns
    original_temporal = extract_temporal_patterns(original_file)
    anonymized_temporal = extract_temporal_patterns(anonymized_file)

    # Step 3: Calculate averages for both datasets
    original_avg = calculate_average(original_features)
    anonymized_avg = calculate_average(anonymized_features)

    # Step 4: Match IDs based on combined similarity
    matched_ids = match_ids(original_avg, anonymized_avg, original_temporal, anonymized_temporal)

    # Step 5: Write results to output file
    with open(output_file, 'w') as f:
        json.dump(matched_ids, f, indent=4)

# Example usage
if __name__ == "__main__":
    
    # original_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_origin/survey_results_1.csv"  
    # anonymized_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_ano/ano_1.csv"   
    # output_json = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/attack_phase/output/combined_attack_data_1.json" 

    # # Run the attack
    # combined_attack(original_file, anonymized_file, output_json)

    # original_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_origin/survey_results_2.csv"  
    # anonymized_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_ano/ano_2.csv"   
    # output_json = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/attack_phase/output/combined_attack_data_2.json" 

    # # Run the attack
    # combined_attack(original_file, anonymized_file, output_json)

    # original_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_origin/survey_results_3.csv"  
    # anonymized_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_ano/ano_3.csv"   
    # output_json = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/attack_phase/output/combined_attack_data_3.json" 

    # # Run the attack
    # combined_attack(original_file, anonymized_file, output_json)

########################################################################################################################

    original_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_origin/survey_results.csv"  
    anonymized_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_ano/anonymized_survey_data.csv"   
    output_json = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/attack_phase/output/combined_attack_survey_data.json" 

    # Run the attack
    combined_attack(original_file, anonymized_file, output_json)

    original_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_origin/big_survey_results.csv"  
    anonymized_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_ano/anonymized_big_survey_data.csv"   
    output_json = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/attack_phase/output/combined_attack_big_survey_data.json" 

    # Run the attack
    combined_attack(original_file, anonymized_file, output_json)

    original_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_origin/bigger_survey_results.csv"  
    anonymized_file = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/metrics/anonymisation/file_ano/anonymized_bigger_survey_data.csv"   
    output_json = "D:/INSA/semetre 7/projet/Anonym/INSAnonym-master-serv/INSAnonym-master/scripts/attack_phase/output/combined_attack_bigger_survey_data.json" 

    # Run the attack
    combined_attack(original_file, anonymized_file, output_json)


