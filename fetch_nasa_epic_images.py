import os
import requests
import json

from pathlib import Path
from dotenv import load_dotenv


def fetch_nasa_epic(folder):
	api_key = os.environ['NASA_API_KEY']
	nasa_folder_name = "nasa_epic"
	params = {
	"api_key": api_key
	}
	archive_url = "https://api.nasa.gov/EPIC/archive/natural/"
	actual_dates_url = "https://api.nasa.gov/EPIC/api/natural/all"
	actual_dates = requests.get(actual_dates_url, params=params)
	actual_dates.raise_for_status()
	last_actual_date = actual_dates.json()[0]['date']
	formatted_date = last_actual_date.replace('-','/')
	last_actual_date_url = f"https://api.nasa.gov/EPIC/api/natural/date/{last_actual_date}"
	response = requests.get(last_actual_date_url, params=params)
	response.raise_for_status()
	last_archive = response.json()
	Path(f"./{folder}/{nasa_folder_name}/").mkdir(parents=True, exist_ok=True)
	image_id = 0
	for element in last_archive:
		epic_image_url = f"{archive_url}{formatted_date}/png/{element['image']}.png"
		response = requests.get(epic_image_url, params=params)
		response.raise_for_status()
		image_name = f'nasa_epic_{last_actual_date}_{image_id}.png'
		with open(f"./{folder}/{nasa_folder_name}/{image_name}", "wb") as file:
			file.write(response.content)
		image_id += 1


def main():
	load_dotenv()
	images_folder_name = 'images'
	Path(f"./{images_folder_name}").mkdir(parents=True, exist_ok=True)
	fetch_nasa_epic(images_folder_name)


if __name__ == "__main__":
	main()
