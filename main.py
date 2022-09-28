import requests

from pathlib import Path


def download_and_save_image(url, folder):
	response = requests.get(url)
	response.raise_for_status()
	filename = 'hubble.jpeg'
	with open(f"./{folder}/{filename}", "wb") as file:
		file.write(response.content)


def main():
	url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"
	images_folder_name = 'images'
	Path(f"./{images_folder_name}").mkdir(parents=True, exist_ok=True)
	download_and_save_image(url, images_folder_name)


if __name__ == "__main__":
	main()
