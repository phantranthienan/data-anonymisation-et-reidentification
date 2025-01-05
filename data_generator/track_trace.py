# import pandas as pd
# import folium
# import random

# def track_individual_markers(input_file, output_html="geo_marker_map.html"):
#     """
#     Tracks geolocation data as individual markers with unique colors for each person.
    
#     Args:
#         input_file (str): Path to the CSV file with geolocation data.
#         output_html (str): Output HTML file for the map visualization.
#     """
#     # Load the data
#     df = pd.read_csv(input_file)
    
#     # Ensure the data is sorted by ID and Date
#     df["Date"] = pd.to_datetime(df["Date"])
#     df = df.sort_values(by=["ID", "Date"])
    
#     # Initialize a Folium map centered at the average location
#     initial_location = [df["Latitude"].mean(), df["Longitude"].mean()]
#     geo_map = folium.Map(location=initial_location, zoom_start=12)

#     # Generate unique colors for each person
#     unique_ids = df["ID"].unique()
#     color_palette = [
#         f"#{random.randint(0, 0xFFFFFF):06x}" for _ in unique_ids
#     ]  # Generate random hex colors
#     id_to_color = dict(zip(unique_ids, color_palette))

#     # Add CircleMarkers for each person
#     for person_id, group in df.groupby("ID"):
#         color = id_to_color[person_id]
#         for _, row in group.iterrows():
#             folium.CircleMarker(
#                 location=[row["Latitude"], row["Longitude"]],
#                 radius=5,
#                 popup=f"{person_id}<br>{row['Date']}",
#                 color=color,
#                 fill=True,
#                 fill_color=color,
#                 fill_opacity=0.6,
#             ).add_to(geo_map)

#     # Save the map to an HTML file
#     geo_map.save(output_html)
#     print(f"Map has been saved to {output_html}")

# # Example usage
# track_individual_markers("geo_data.csv", "geo_marker_map.html")


import pandas as pd
import folium
import random

def track_individual_markers_with_icons(input_file, output_html="geo_marker_map.html"):
    """
    Tracks geolocation data as individual markers with unique predefined colors for each person.
    
    Args:
        input_file (str): Path to the CSV file with geolocation data.
        output_html (str): Output HTML file for the map visualization.
    """
    # Load the data
    df = pd.read_csv(input_file)
    
    # Ensure the data is sorted by ID and Date
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(by=["ID", "Date"])
    
    # Initialize a Folium map centered at the average location
    initial_location = [df["Latitude"].mean(), df["Longitude"].mean()]
    geo_map = folium.Map(location=initial_location, zoom_start=12)

    # Predefined Folium colors
    folium_colors = [
        "red", "blue", "green", "purple", "orange", "darkred", "lightred", 
        "beige", "darkblue", "darkgreen", "cadetblue", "pink", "lightblue", 
        "lightgreen", "gray", "black", "lightgray"
    ]

    # Assign colors to each person (looping through Folium's color palette if necessary)
    unique_ids = df["ID"].unique()
    id_to_color = {person_id: folium_colors[i % len(folium_colors)] for i, person_id in enumerate(unique_ids)}

    # Add markers for each person
    for person_id, group in df.groupby("ID"):
        color = id_to_color[person_id]
        for _, row in group.iterrows():
            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                popup=f"{person_id}<br>{row['Date']}",
                icon=folium.Icon(color=color, icon="info-sign", prefix="fa"),
            ).add_to(geo_map)

    # Save the map to an HTML file
    geo_map.save(output_html)
    print(f"Map has been saved to {output_html}")

# Example usage
track_individual_markers_with_icons("geo_data.csv", "geo_marker_map.html")