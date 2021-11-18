import os
import time
import requests
import datetime
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlsplit
import telegram


def publish_telegram(file_name):
    bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT"))
    time.sleep(int(os.getenv("LATENCY_SECONDS", default=86400)))
    bot.send_photo(chat_id=os.getenv("GROUP_ID"), photo=open(f"{file_name}", "rb"))


def create_image_folder():
    Path("./images/").mkdir(parents=True, exist_ok=True)


def fetch_spacex_last_launch():
    response = requests.get("https://api.spacexdata.com/v3/launches")
    response.raise_for_status()
    images_launches = (response.json()[107].get("links").get("flickr_images"))
    write_files(images_launches, "spacex")


def write_files(links_of_images, image_name):
    for image_number, image_value in enumerate(links_of_images):
        with open(f"images/{image_name}{image_number}{get_file_ext(image_value)}", "wb") as file:
            file.write(requests.get(image_value).content)
            publish_telegram(f"images/{image_name}{image_number}{get_file_ext(image_value)}")


def fetch_nasa_apod(nasa_api):
    apod_link = "https://api.nasa.gov/planetary/apod"
    params = {
        "count": 3,
        "api_key": f"{nasa_api}",
    }
    nasa_images = []
    response = requests.get(apod_link, params)
    response.raise_for_status()
    for apod_image in response.json():
        nasa_images.append(apod_image.get("hdurl"))
    write_files(nasa_images, "nasa")


def fetch_nasa_epic(nasa_api):
    epic_link = f"https://api.nasa.gov/EPIC/api/natural"
    params = {
        "api_key": f"{nasa_api}",
    }
    response = requests.get(epic_link, params)
    images_list = []
    for epic_image in response.json():
        image_date = datetime.datetime.fromisoformat(epic_image.get('date'))
        images_list.append(f"https://api.nasa.gov/EPIC/archive/natural/"
                           f"{image_date.year}/{image_date.month}/{image_date.day}/"
                           f"png/{epic_image.get('image')}.png?api_key={nasa_api}")
    write_files(images_list, "nasa_epic")


def get_file_ext(ext_link):
    ext_link = urlsplit(ext_link)
    return os.path.splitext(ext_link.path)[1]


def main():
    while True:
        load_dotenv()
        create_image_folder()
        nasa_api = os.getenv("NASA_API")
        fetch_nasa_apod(nasa_api)
        fetch_spacex_last_launch()
        fetch_nasa_epic(nasa_api)


if __name__ == "__main__":
    main()
