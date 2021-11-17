## The NASA API  
This project will download photos from NASA APOD, NASA EPIC, SpaceX and will save on local folder. After that, photos are published on telegram channel.

## Requirements  
python==3.10.0  
python-dotenv==0.19.2  
python_telegram_bot==13.8.1  
requests==2.26.0  
telegram==0.0.1  



## How to install  
Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:  
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
## How to start
just launch main.py
```
Publish-media-content-telegram % python3 main.py 
Publish-media-content-telegram % ls -la images 
total 80616
drwxr-xr-x  21 asivolap  staff      672 Nov 15 19:19 .
drwxr-xr-x  10 asivolap  staff      320 Nov 15 19:19 ..
-rw-r--r--   1 asivolap  staff   465891 Nov 15 19:19 nasa0.jpg
-rw-r--r--   1 asivolap  staff  1008425 Nov 15 19:19 nasa1.jpg
-rw-r--r--   1 asivolap  staff   181855 Nov 15 19:19 nasa2.jpg
-rw-r--r--   1 asivolap  staff  2670302 Nov 15 19:19 nasa_epic0.png
-rw-r--r--   1 asivolap  staff  2761943 Nov 15 19:19 nasa_epic1.png
-rw-r--r--   1 asivolap  staff  2682067 Nov 15 19:19 nasa_epic2.png
-rw-r--r--   1 asivolap  staff  2698721 Nov 15 19:19 nasa_epic3.png
-rw-r--r--   1 asivolap  staff  2596591 Nov 15 19:19 nasa_epic4.png
-rw-r--r--   1 asivolap  staff  2678010 Nov 15 19:19 nasa_epic5.png
-rw-r--r--   1 asivolap  staff  2702940 Nov 15 19:19 nasa_epic6.png
-rw-r--r--   1 asivolap  staff  2686540 Nov 15 19:19 nasa_epic7.png
-rw-r--r--   1 asivolap  staff  2796250 Nov 15 19:19 nasa_epic8.png
-rw-r--r--   1 asivolap  staff  2792580 Nov 15 19:20 nasa_epic9.png
-rw-r--r--   1 asivolap  staff  2205424 Nov 15 19:19 spacex0.jpg
-rw-r--r--   1 asivolap  staff  1604275 Nov 15 19:19 spacex1.jpg
-rw-r--r--   1 asivolap  staff  1982955 Nov 15 19:19 spacex2.jpg
-rw-r--r--   1 asivolap  staff  2453952 Nov 15 19:19 spacex3.jpg
-rw-r--r--   1 asivolap  staff  2267684 Nov 15 19:19 spacex4.jpg
-rw-r--r--   1 asivolap  staff  2007854 Nov 15 19:19 spacex5.jpg
```

![Telegram_image](https://i.ibb.co/YZwY2B6/Screenshot-2021-11-17-at-20-33-23.png)
