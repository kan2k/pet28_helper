import requests
import json

pets_filename = "catto.txt"
filtered_pets = []

for i in range(1, 5):
    url = (
        "https://pet28.com/api/public/pet/listing/2/"
        + str(i)
        + "/?searchParams=%7B%22keyword%22:%22%E5%B8%83%E5%81%B6%22%7D"
    )
    response = requests.get(url)
    json_data = json.loads(response.content)
    pets = json_data["adopt"] + json_data["buy"]
    for pet in pets:
        if "猫" in pet["title"]:
            continue
        detail_url = "https://pet28.com/api/public/pet/details/" + pet["id"] + "/"
        detail_response = requests.get(detail_url)
        detail = json.loads(detail_response.content)
        # 'bday': '2021-01-01'
        if detail["bday"].split("-")[0] != "2021":
            continue
        if "wechat" in detail["content"].lower():
            continue
        link = "https://pet28.com/pet/cat/" + str(detail["id"])
        candidate = {
            "id": detail["id"],
            "name": detail["title"],
            "content": detail["content"],
            "sex": detail["sex"],
            "birth": detail["bday"],
            "link": link,
        }
        filtered_pets.append(candidate)

# clear and write file
open(pets_filename, "w")
with open(pets_filename, mode="w", encoding="utf-8") as file:
    for pet in filtered_pets:
        file.write("------------------------------------\n")
        file.write(pet["id"] + "\n")
        file.write(pet["name"] + "\n")
        file.write(pet["sex"] + "\n")
        file.write(pet["content"] + "\n")
        file.write(pet["birth"] + "\n")
        file.write(pet["link"] + "\n")
        file.write("------------------------------------\n")

print("found", len(filtered_pets), "pets! :)")
