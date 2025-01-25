import zipfile
import os

def zip_csv_file(csv_file_path, zip_file_path):
    """
    Compress a CSV file into a .zip archive.

    Parameters:
        csv_file_path (str): The full path to the CSV file to be zipped.
        zip_file_path (str): The full path for the output .zip file.

    Returns:
        bool: True if the operation is successful, False otherwise.
    """
    try:
        # Check if the CSV file exists
        if not os.path.exists(csv_file_path):
            print(f"Error: The file {csv_file_path} does not exist.")
            return False
        
        # Create a ZIP file and add the CSV file to it
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_file_path, os.path.basename(csv_file_path))
        
        print(f"Successfully created {zip_file_path}")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Example Usage
csv_file = "file_origin/big_survey_results.csv"   # Replace with your CSV file path
zip_file = "./origin.zip"  # Replace with your desired ZIP file path
zip_csv_file(csv_file, zip_file)