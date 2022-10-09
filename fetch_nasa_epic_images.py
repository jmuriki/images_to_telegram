import os
import requests
import json

from dotenv import load_dotenv

from multifunctional_module import create_folder_safely
from multifunctional_module import get_response
from multifunctional_module import compose_filename
from multifunctional_module import save_content


def get_dates(api_param):
	all_epic_actual_dates_url = "https://api.nasa.gov/EPIC/api/natural/all"
	all_actual_dates = get_response(all_epic_actual_dates_url, api_param).json()
	last_actual_date = all_actual_dates[0]["date"]
	last_actual_date_formatted = last_actual_date.replace("-","/")
	return last_actual_date, last_actual_date_formatted


def get_last_archive(last_actual_date_url, api_param):
	last_actual_date_url = f"https://api.nasa.gov/EPIC/api/natural/date/{last_actual_date_url}"
	last_archive = get_response(last_actual_date_url, api_param).json()
	return last_archive


def get_epic_image_url(date_formatted, image_name, extention):
	epic_archive_url = "https://api.nasa.gov/EPIC/archive/natural/"
	epic_image_url = f"{epic_archive_url}{date_formatted}/png/{image_name}{extention}"
	return epic_image_url


def fetch_nasa_epic(api_param, main_images_folder):
	nasa_epic_folder = create_folder_safely(main_images_folder, "nasa_epic")
	date, date_formatted = get_dates(api_param)
	archive = get_last_archive(date, api_param)
	extention = ".png"
	for epic_index, epic in enumerate(archive):
		url = get_epic_image_url(date_formatted, epic['image'], extention)
		filename = compose_filename(nasa_epic_folder, date, epic_index, extention)
		content = get_response(url, api_param).content
		save_content(main_images_folder, filename, content, nasa_epic_folder)


def main():
	load_dotenv()
	api_key = os.environ["NASA_API_KEY"]
	api_param = ["api_key", api_key]
	main_images_folder = create_folder_safely()
	fetch_nasa_epic(api_param, main_images_folder)


if __name__ == "__main__":
	main()
