import requests

from pathlib import Path


def main():
	images_folder_name = 'images'
	filename = 'hubble.jpeg'
	url = "https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg"
	response = requests.get(url)
	response.raise_for_status()
	Path(f"./{images_folder_name}").mkdir(parents=True, exist_ok=True)
	with open(f"./{images_folder_name}/{filename}", "wb") as file:
		file.write(response.content)


if __name__ == "__main__":
	main()
