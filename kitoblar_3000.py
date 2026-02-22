import requests
import os
import time

API_KEY = "4mOlYE8QAyHZSuPwOaL1QzPQgPJW95fOXVXlBJ5MspgWAV9ZKdS0bmpU"
BASE_URL = "https://api.pexels.com/v1/search"

TARGET_TOTAL = 3000
PER_PAGE = 80

queries = [
    "books",
    "library",
    "bookshelf",
    "reading book",
    "open book",
    "stack of books",
    "study books"
]

SAVE_FOLDER = "books_dataset"
os.makedirs(SAVE_FOLDER, exist_ok=True)

headers = {
    "Authorization": API_KEY
}

existing_files = [f for f in os.listdir(SAVE_FOLDER) if f.endswith(".jpg")]
downloaded = len(existing_files)

print(f"Hozir {downloaded} ta rasm bor.")

if downloaded >= TARGET_TOTAL:
    print("Allaqachon 3000 ta bor.")
    exit()

for query in queries:
    page = 1

    while downloaded < TARGET_TOTAL:
        params = {
            "query": query,
            "per_page": PER_PAGE,
            "page": page
        }

        response = requests.get(BASE_URL, headers=headers, params=params)

        if response.status_code != 200:
            print("API limit yoki xatolik:", response.status_code)
            break

        data = response.json()
        photos = data.get("photos", [])

        if not photos:
            break

        for photo in photos:
            if downloaded >= TARGET_TOTAL:
                break

            img_url = photo["src"]["medium"]
            img_data = requests.get(img_url).content

            file_name = f"book_{downloaded+1}.jpg"
            file_path = os.path.join(SAVE_FOLDER, file_name)

            with open(file_path, "wb") as f:
                f.write(img_data)

            downloaded += 1
            print(f"{downloaded}-rasm yuklandi")

            time.sleep(0.2)

        page += 1

print("✅ Tugadi!")
print(f"Jami {downloaded} ta rasm bor.")