import csv
import datetime
from Utils import separator  # Define your custom separator (e.g., '\t', ',')

# Define activity categories and time ranges
activity_time_ranges = {
    "work": (9, 17),  # 9:00 AM to 5:00 PM
    "leisure": (17, 22),  # 5:00 PM to 10:00 PM
    "sleep": (22, 6),  # 10:00 PM to 6:00 AM
    "travel": (6, 9)  # 6:00 AM to 9:00 AM
}

def categorize_time(time_obj):
    """
    Categorizes the time of day into predefined activities based on time ranges.
    :param time_obj: A time object representing a specific time of day.
    :return: Activity category (e.g., "work", "leisure", "sleep", "travel").
    """
    for activity, (start, end) in activity_time_ranges.items():
        if start <= time_obj.hour < end or (start > end and (time_obj.hour >= start or time_obj.hour < end)):
            return activity
    return "unknown"

def calculate_time_spent(data):
    """
    Calculate the total time spent in each activity category from a list of timestamps.
    :param data: List of datetime objects representing the user's activities.
    :return: Dictionary with total time spent in each activity.
    """
    activity_time = {activity: datetime.timedelta() for activity in activity_time_ranges}
    
    for timestamp in data:
        activity = categorize_time(timestamp.time())
        activity_time[activity] += datetime.timedelta(hours=1)  # Assuming 1 hour per entry for simplicity
    
    return activity_time

def calculate_score(original_time, anonymised_time):
    """
    Calculate the score based on the comparison of time spent in each activity category.
    :param original_time: Time spent in activities in the original dataset.
    :param anonymised_time: Time spent in activities in the anonymized dataset.
    :return: The time usage consistency score.
    """
    score = 0
    total_activities = len(original_time)
    
    for activity in original_time:
        original_duration = original_time[activity].total_seconds()
        anonymised_duration = anonymised_time[activity].total_seconds()
        
        if original_duration > anonymised_duration:
            score += anonymised_duration / original_duration
        else:
            score += original_duration / anonymised_duration
    
    return score / total_activities

def main(originalFile, anonymisedFile, parameters=None):
    """
    Compare time usage patterns between the original and anonymized dataset.
    
    :param originalFile: Path to the original dataset file.
    :param anonymisedFile: Path to the anonymized dataset file.
    :param parameters: Optional parameters for customization.
    :return: Time usage consistency score.
    """
    # Open original and anonymized files
    fd_original = open(originalFile, newline='')
    fd_anonymised = open(anonymisedFile, newline='')
    
    original_reader = csv.reader(fd_original, delimiter=separator)
    anonymised_reader = csv.reader(fd_anonymised, delimiter=separator)

    original_data = []
    anonymised_data = []
    
    # Process the data and extract timestamps
    for lineOri, lineAno in zip(original_reader, anonymised_reader):
        # Original data timestamp
        original_timestamp = datetime.datetime.fromisoformat(lineOri[1][:19])
        original_data.append(original_timestamp)
        
        # Anonymized data timestamp
        anonymised_timestamp = datetime.datetime.fromisoformat(lineAno[1][:19])
        anonymised_data.append(anonymised_timestamp)
    
    # Calculate the total time spent in each activity category
    original_time_spent = calculate_time_spent(original_data)
    anonymised_time_spent = calculate_time_spent(anonymised_data)
    
    # Calculate the score
    score = calculate_score(original_time_spent, anonymised_time_spent)
    
    return score
