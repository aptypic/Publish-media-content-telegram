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
        time.sleep(int(latency_seconds))
        with open(f"images/{image}", "rb") as file:
            bot.send_photo(chat_id=telegram_group_id, photo=file)


def get_env_values(key):
    return os.getenv(f"{key}")


def create_image_folder():
    Path("./images/").mkdir(parents=True, exist_ok=True)


def fetch_spacex_last_launch():
    response = requests.get("https://api.spacexdata.com/v3/launches")
    response.raise_for_status()
    write_files(define_latest_launch(), "spacex")


def define_latest_launch():
    response = requests.get("https://api.spacexdata.com/v3/launches")
    response.raise_for_status()
    for launch in reversed(response.json()):
        if not launch.get("links").get("flickr_images"):
            pass
        else:
            return launch.get("links").get("flickr_images")


def write_files(links_of_images, image_name):
    for image_number, image_value in enumerate(links_of_images):
        with open(f"images/{image_name}{image_number}{get_file_ext(image_value)}", "wb") as file:
            file.write(requests.get(image_value).content)


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
    write_files(nasa_images, "nasa")


def fetch_nasa_epic(nasa_api):
    epic_link = f"https://api.nasa.gov/EPIC/api/natural"
    params = {
        "api_key": f"{nasa_api}",
    }
    response = requests.get(epic_link, params)
    response.raise_for_status()
    images_list = []
    for epic_image in response.json():
        image_date = datetime.datetime.fromisoformat(epic_image.get("date"))
        images_list.append(requests.get(f"https://api.nasa.gov/EPIC/archive/natural/"
                                        f"{image_date.year}/{image_date.month}/{image_date.day}/"
                                        f"png/{epic_image.get('image')}.png", params=params).url)
        print(images_list)
    write_files(images_list, "nasa_epic")


def get_file_ext(ext_link):
    ext_link = urlsplit(ext_link)
    return os.path.splitext(ext_link.path)[1]


def main():
    while True:
        load_dotenv()
        create_image_folder()
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
