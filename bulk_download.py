"""This file is for downloading the blurry images of snakes, cats and dogs to improve the performance of the model, not related with 
the main program running and grading. This file is not original."""

import requests
import os
import time
import cv2
from PIL import Image
from io import BytesIO
import numpy as np

ACCESS_KEY = '9t8kamZoEG3-kSv1x9hx-Gm6lrahxz63kTvmT2Zp-34'
QUERY = 'dog'
TOTAL_BLURRY_IMAGES = 1000
IMAGES_PER_PAGE = 30
SAVE_FOLDER = '/Users/lora/desktop/bcog200/final_project_submit/keras-cats-dogs-tutorial/catsdogs/sample/train/dogs'
BLUR_THRESHOLD = 15  # Lower = more blurry

os.makedirs(SAVE_FOLDER, exist_ok=True)

def is_blurry(img, threshold=BLUR_THRESHOLD):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return var < threshold

def download_blurry_images():
    blurry_count = 0
    page = 1
    seen_ids = set()

    while blurry_count < TOTAL_BLURRY_IMAGES and page <= 100:
        print(f"\nFetching page {page}...")
        url = f'https://api.unsplash.com/search/photos?page={page}&per_page={IMAGES_PER_PAGE}&query={QUERY}&client_id={ACCESS_KEY}'
        response = requests.get(url)

        # 🛑 Handle rate limit (HTTP 429)
        if response.status_code == 429:
            print("⚠️ Rate limit hit. Waiting 60 minutes before retrying...")
            time.sleep(3600)
            continue

        if response.status_code != 200:
            print("❌ Failed to fetch images:", response.text)
            break

        data = response.json()
        results = data.get("results", [])

        if not results:
            print("No results found.")
            break

        for result in results:
            image_id = result['id']
            if image_id in seen_ids:
                continue
            seen_ids.add(image_id)

            image_url = result['urls']['regular']
            try:
                img_data = requests.get(image_url).content
                img = Image.open(BytesIO(img_data)).convert('RGB')
                img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

                if is_blurry(img_cv):
                    path = os.path.join(SAVE_FOLDER, f"{image_id}.jpg")
                    with open(path, 'wb') as f:
                        f.write(img_data)
                    blurry_count += 1
                    print(f"✅ Saved blurry image {blurry_count}: {path}")

                    if blurry_count >= TOTAL_BLURRY_IMAGES:
                        break
                else:
                    print("❌ Not blurry enough.")

            except Exception as e:
                print("⚠️ Error:", e)
                continue

        page += 1
        time.sleep(1)

    print(f"\n🎉 Finished downloading {blurry_count} blurry dog images.")

download_blurry_images()
