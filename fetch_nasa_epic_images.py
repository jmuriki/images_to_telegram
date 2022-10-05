import os
import requests
import json

from dotenv import load_dotenv

from multifunctional_module import create_folder_safely
from multifunctional_module import get_response
from multifunctional_module import compose_filename
from multifunctional_module import download_content
from multifunctional_module import save_content


def fetch_nasa_epic(api_key, main_images_folder):
	nasa_epic_folder = create_folder_safely(main_images_folder, "nasa_epic")
	epic_archive_url = "https://api.nasa.gov/EPIC/archive/natural/"
	all_actual_dates_url = "https://api.nasa.gov/EPIC/api/natural/all"
	api_param = ["api_key", api_key]
	all_actual_dates = get_response(all_actual_dates_url, api_param).json()
	last_actual_date = all_actual_dates[0]["date"]
	last_actual_date_formatted = last_actual_date.replace("-","/")
	last_actual_date_url = f"https://api.nasa.gov/EPIC/api/natural/date/{last_actual_date}"
	last_archive = get_response(last_actual_date_url, api_param).json()
	image_id = 0
	for epic in last_archive:
		extention = ".png"
		epic_image_url = f"{epic_archive_url}{last_actual_date_formatted}/png/{epic['image']}{extention}"
		filename = compose_filename(nasa_epic_folder, last_actual_date, image_id, extention)
		content = download_content(epic_image_url, api_param)
		save_content(main_images_folder, filename, content, nasa_epic_folder)
		image_id += 1


def main():
	load_dotenv()
	api_key = os.environ["NASA_API_KEY"]
	main_images_folder = create_folder_safely()
	fetch_nasa_epic(api_key, main_images_folder)


if __name__ == "__main__":
	main()
