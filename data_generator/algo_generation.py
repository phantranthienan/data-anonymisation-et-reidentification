import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np


def gaussian_coordinates(center, std_dev_km):
    """
    Generate random coordinates following a Gaussian distribution around a center point.
    
    Args:
        center (tuple): Center point (latitude, longitude).
        std_dev_km (float): Standard deviation in kilometers. (how spread out the data points are around the mean (center of the city))
        
    Returns:
        tuple: Generated (latitude, longitude) coordinates.
    """
    lat, lon = center
    std_dev_deg = std_dev_km / 111  # Convert standard deviation from km to degrees
    rand_lat = np.random.normal(lat, std_dev_deg)
    rand_lon = np.random.normal(lon, std_dev_deg)
    return round(rand_lat, 6), round(rand_lon, 6)  # 6 decimal places


def generate_realistic_geo_data_with_groups_gaussian(position, time_interval, number_of_people, output_file="geo_data_gaussian.csv"):
    """
    Generate realistic geolocation data using Gaussian distribution for three groups: home-work, home-only, and random-only.

    Args:
        position (tuple): Center point of the city (latitude, longitude).
        time_interval (tuple): Start and end date in the format ("YYYY-MM-DD", "YYYY-MM-DD").
        number_of_people (int): Number of unique individuals.
        output_file (str): File name for the output CSV.

    Returns:
        None. Saves the data to the specified output file.
    """
    city_std_dev_km = 3  # Standard deviation for the city in km
    home_std_dev_km = 1  # Smaller spread for home or work
    # Parse time interval
    start_date = datetime.strptime(time_interval[0], "%Y-%m-%d")
    end_date = datetime.strptime(time_interval[1], "%Y-%m-%d")
    num_days = (end_date - start_date).days + 1

    # Define group proportions
    group_proportions = {
        "home_work": 0.5,
        "home_only": 0.3,
        "random_only": 0.2,
    }

    # Assign group membership
    groups = random.choices(
        population=["home_work", "home_only", "random_only"],
        weights=[group_proportions["home_work"], group_proportions["home_only"], group_proportions["random_only"]],
        k=number_of_people,
    )

    # Generate geolocation data
    data = []
    for person_id in range(1, number_of_people + 1):
        person_id_str = f"Person_{person_id}"
        group = groups[person_id - 1]

        # Assign home and work locations if needed
        home_coords = gaussian_coordinates(position, home_std_dev_km)
        work_coords = gaussian_coordinates(position, home_std_dev_km) if group == "home_work" else None

        # Randomly decide the days this person has data
        active_days = random.sample(range(num_days), k=random.randint(num_days // 2, int(num_days * 0.75)))  # Active 50%-75% days
        for day_offset in active_days:
            date = start_date + timedelta(days=day_offset)

            # Randomly select one period for the day
            period = random.choice(["morning", "afternoon", "evening", "night"])

            if group == "home_work":
                if period == "night":  # Night at home
                    timestamp = datetime.combine(date, datetime.min.time()) + timedelta(hours=random.randint(22, 23), minutes=random.randint(0, 59))
                    lat, lon = gaussian_coordinates(home_coords, home_std_dev_km)
                elif period in ["morning", "afternoon"]:  # Work hours
                    timestamp = datetime.combine(date, datetime.min.time()) + timedelta(hours=random.randint(9, 17), minutes=random.randint(0, 59))
                    lat, lon = gaussian_coordinates(work_coords, home_std_dev_km)
                else:  # Evening random activities
                    timestamp = datetime.combine(date, datetime.min.time()) + timedelta(hours=random.randint(18, 21), minutes=random.randint(0, 59))
                    lat, lon = gaussian_coordinates(position, city_std_dev_km)

            elif group == "home_only":
                if period == "night":  # Night at home
                    timestamp = datetime.combine(date, datetime.min.time()) + timedelta(hours=random.randint(22, 23), minutes=random.randint(0, 59))
                    lat, lon = gaussian_coordinates(home_coords, home_std_dev_km)
                else:  # Random activities during the day near home
                    timestamp = datetime.combine(date, datetime.min.time()) + timedelta(hours=random.randint(6, 21), minutes=random.randint(0, 59))
                    lat, lon = gaussian_coordinates(home_coords, home_std_dev_km)

            elif group == "random_only":
                # Randomly move anywhere in the city
                timestamp = datetime.combine(date, datetime.min.time()) + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
                lat, lon = gaussian_coordinates(position, city_std_dev_km)

            # Append data
            data.append({
                "ID": person_id_str,
                "Date": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "Latitude": lat,
                "Longitude": lon,
            })

    # Save to CSV
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Generated geolocation data saved to {output_file}")


# Example usage
generate_realistic_geo_data_with_groups_gaussian(
    position=(48.8566, 2.3522),  # Center point (e.g., Paris)
    time_interval=("2024-10-01", "2024-10-30"),  # Time interval
    number_of_people=10,  # Number of individuals
    output_file="../geo_data.csv"
)

"""
This algorithm generates synthetic geolocation data for individuals using Gaussian distribution to simulate realistic movement patterns. It categorizes individuals into three groups:
	1.	Home-Work Group: Activities occur near fixed home and work locations, with occasional movements throughout the city.
	2.	Home-Only Group: Activities are concentrated around a single home location.
	3.	Random-Only Group: Movements occur randomly within the city.

Key features:
	•	Geolocation Simulation: Coordinates are generated based on Gaussian distribution, centering on home, work, or city locations, creating realistic clustering.
    (Gaussian distribution can effectively model this concept by creating higher data points near the city center, tapering off gradually toward the outskirts.)
	•	Temporal Activity Patterns: Each individual is active 50%-75% of days, with activities distributed across morning, afternoon, evening, and night.
	•	Behavioral Diversity: Individuals exhibit distinct movement behaviors, mirroring real-world variability.

Output:
	•	A CSV file containing ID, Date, Latitude, and Longitude, representing the simulated geolocation data.
"""