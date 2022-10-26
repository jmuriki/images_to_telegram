import os
import requests
import datetime

from dotenv import load_dotenv
from multifunctional_module import create_folder_safely
from multifunctional_module import compose_filepath
from multifunctional_module import save_content


def get_dates(api_param):
    url = "https://api.nasa.gov/EPIC/api/natural/all"
    response = requests.get(url, api_param)
    response.raise_for_status()
    return response.json()


def format_date(iso_date):
    date = datetime.datetime.fromisoformat(iso_date).date()
    return date.strftime("%Y/%m/%d")


def get_archive(date, api_param):
    url = f"https://api.nasa.gov/EPIC/api/natural/date/{date}"
    response = requests.get(url, api_param)
    response.raise_for_status()
    archive = response.json()
    return archive


def get_epic_url(formatted_date, image_name):
    url = "https://api.nasa.gov/EPIC/archive/natural/"
    epic_url = f"{url}{formatted_date}/png/{image_name}.png"
    return epic_url


def fetch_images(api_param, main_folder):
    secondary_folder = create_folder_safely(main_folder, "nasa_epic")
    iso_date = get_dates(api_param)[0]["date"]
    formatted_date = format_date(iso_date)
    archive = get_archive(iso_date, api_param)
    for index, epic in enumerate(archive, start=1):
        epic_url = get_epic_url(formatted_date, epic["image"])
        filepath = compose_filepath(
            epic_url,
            main_folder,
            iso_date,
            secondary_folder,
            index,
        )
        save_content(epic_url, filepath, api_param)


def main():
    load_dotenv()
    api_key = os.environ["NASA_API_KEY"]
    api_param = {"api_key": api_key}
    main_folder = create_folder_safely()
    fetch_images(api_param, main_folder)


if __name__ == "__main__":
    main()
