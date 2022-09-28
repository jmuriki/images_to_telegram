import requests
import json

from pathlib import Path


def fetch_spacex_last_launch(images_folder_name):
	space_x_api_url = "https://api.spacexdata.com/v5/launches/"
	response = requests.get(space_x_api_url)
	response.raise_for_status()
	for launche in response.json()[::-1]:
		links = launche['links']['flickr']['original']
		if links:
			for link_number, link in enumerate(links):
				response = requests.get(link)
				response.raise_for_status()
				filename = f'spacex_{link_number}.jpg'
				with open(f"./{images_folder_name}/{filename}", "wb") as file:
					file.write(response.content)
			break


def main():
	images_folder_name = 'images'
	Path(f"./{images_folder_name}").mkdir(parents=True, exist_ok=True)
	fetch_spacex_last_launch(images_folder_name)


if __name__ == "__main__":
	main()
