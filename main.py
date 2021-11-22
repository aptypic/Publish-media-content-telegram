import os
import time
import requests
import datetime
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlsplit
import telegram


def publish_telegram(token, latency_seconds, telegram_group_id):
    bot = telegram.Bot(token=token)
    for image in os.listdir("images/"):
        with open(f"images/{image}", "rb") as file:
            bot.send_photo(chat_id=telegram_group_id, photo=file)
        time.sleep(int(latency_seconds))


def fetch_spacex_last_launch():
    response = requests.get("https://api.spacexdata.com/v3/launches")
    response.raise_for_status()
    download_images(define_latest_launch(response), "spacex")


def define_latest_launch(response):
    for launch in reversed(response.json()):
        if launch.get("links").get("flickr_images"):
            return launch.get("links").get("flickr_images")


def download_images(links_of_images, image_name, params={}):
    for image_number, image_value in enumerate(links_of_images):
        with open(f"images/{image_name}{image_number}{get_file_ext(image_value)}", "wb") as file:
            response = requests.get(image_value, params)
            response.raise_for_status()
            file.write(response.content)


def fetch_nasa_apod(nasa_api):
    apod_link = "https://api.nasa.gov/planetary/apod"
    params = {
        "count": 3,
        "api_key": nasa_api,
    }
    nasa_images = []
    response = requests.get(apod_link, params)
    response.raise_for_status()
    for apod_image in response.json():
        nasa_images.append(apod_image.get("hdurl"))
    download_images(nasa_images, "nasa", params)


def fetch_nasa_epic(nasa_api):
    epic_link = f"https://api.nasa.gov/EPIC/api/natural"
    params = {
        "api_key": nasa_api,
    }
    response = requests.get(epic_link, params)
    response.raise_for_status()
    links_catalog = []
    for epic_image in response.json():
        image_date = datetime.datetime.fromisoformat(epic_image.get("date"))
        epic_image = f"{epic_image.get('image')}.png"
        year, month, day = image_date.year, image_date.month, image_date.day
        url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{epic_image}"
        links_catalog.append(url)
    download_images(links_catalog, "nasa_epic", params)


def get_file_ext(ext_link):
    ext_link = urlsplit(ext_link)
    return os.path.splitext(ext_link.path)[1]


def main():
    Path("./images/").mkdir(parents=True, exist_ok=True)
    while True:
        load_dotenv()
        nasa_api = os.getenv("NASA_API")
        telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        latency_seconds = os.getenv("LATENCY_SECONDS")
        telegram_group_id = os.getenv("TELEGRAM_GROUP_ID")
        fetch_nasa_apod(nasa_api)
        fetch_spacex_last_launch()
        fetch_nasa_epic(nasa_api)
        publish_telegram(telegram_bot_token, latency_seconds, telegram_group_id)


if __name__ == "__main__":
    main()
