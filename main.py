import os
import json
from dotenv import load_dotenv
from src.jd_processor import process_jd_folder
from src.resume_processor import process_resumes

# Load environment variables from .env file
load_dotenv()

def main():
    """
    Main function to process job descriptions and resumes using a hybrid approach.
    """
    # Folder paths
    jd_folder = r"./Job_description"  # Folder containing job descriptions
    resumes_folder = r"./Resumes"      # Folder containing resumes in PDF format

    # Output files
    jd_output_file = r"jd_key_aspects/Job_description_key_aspects.json"  # JSON file for job description key aspects
    resumes_output_file = r"ranked_resumes.json"  # Output file for ranked resumes

    # Step 1: Process job descriptions
    process_jd_folder(jd_folder, jd_output_file)

    # Step 2: Process resumes and rank them
    process_resumes(jd_output_file, resumes_folder, resumes_output_file)

if __name__ == "__main__":
    main()