import csv
import random
from datetime import datetime, timedelta
import hashlib

def generate_anonymized_id(original_id, week_num):
    """Génère un identifiant anonymisé basé sur l'identifiant original et le numéro de semaine."""
    hash_input = f"{original_id}_W{week_num}".encode()
    hash_digest = hashlib.sha256(hash_input).hexdigest()[:6]
    return f"{hash_digest.upper()}_W{week_num:02d}"

def modify_date_within_week(date_str):
    """Modifie la date (jour et heure) tout en la gardant dans la même semaine."""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    
    weekday = date_obj.weekday()
    random_day_offset = random.randint(0, 6)
    #Make sure the new date is within the same week
    new_date_obj = date_obj + timedelta(days=random_day_offset - weekday)
    
    random_hours = random.randint(0, 23)
    random_minutes = random.randint(0, 59)
    new_date_obj = new_date_obj.replace(hour=random_hours, minute=random_minutes)
    
    # Separate the date and time
    new_date = new_date_obj.strftime("%Y-%m-%d")
    new_time = new_date_obj.strftime("%H:%M:%S")
    
    return new_date, new_time  # Return both date and time separately

def add_noise_to_coordinates(lat, lon):
    """Ajoute un bruit léger aux coordonnées GPS."""
    noise_lat = random.uniform(-0.001, 0.001)
    noise_lon = random.uniform(-0.001, 0.001)
    return round(lat + noise_lat, 6), round(lon + noise_lon, 6)

def anonymize_csv(input_csv, output_csv):
    """Anonymise les données d'un fichier CSV et les écrit dans un autre fichier."""
    with open(input_csv, mode='r') as infile, open(output_csv, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile, delimiter='\t', fieldnames=['Identifiant', 'Date', 'Latitude', 'Longitude'])
        
        # Using writer with space as delimiter and no quoting or escape character
        writer = csv.writer(outfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)

        next(reader)  # Sauter l'en-tête du fichier d'entrée

        for row in reader:
            original_id = row['Identifiant']
            date = row['Date']
            lat = float(row['Latitude'])
            lon = float(row['Longitude'])

            date_obj = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            week_num = date_obj.isocalendar()[1]

            anon_id = generate_anonymized_id(original_id, week_num)
            anon_date, anon_time = modify_date_within_week(date)  # This will remove backslashes
            print(anon_date)
            anon_lat, anon_lon = add_noise_to_coordinates(lat, lon)
            print(anon_lat, anon_lon)
            
            writer.writerow([anon_id, f"{anon_date} {anon_time}", f"{anon_lat:.6f} {anon_lon:.6f}"])

input_csv = 'D:\INSA\semetre 7\projet\Anonym\INSAnonym-master-serv\INSAnonym-master\scripts\origin.csv'
output_csv = 'D:\INSA\semetre 7\projet\Anonym\INSAnonym-master-serv\INSAnonym-master\scripts\\anon.csv'

anonymize_csv(input_csv, output_csv)
