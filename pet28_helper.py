#              Pet28 Helper
#   Jason Kwok - https://github.com/kan2k

from selenium import webdriver
import time
from pprint import pprint

url = "https://pet28.com/pet/cat?keyword=%E5%B8%83%E5%81%B6"  # Paste your search link here

# init selenium
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
browser = webdriver.Chrome(options=options)
browser.get(url)

# scroll to bottom 3 times
for i in range(5):
    time.sleep(1)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# find all pets
time.sleep(1)
unfiltered_links = []
pet_items = []
for i in range(3):
    pet_items = browser.find_elements_by_tag_name("pet-item")
    if len(pet_items) > 0:
        break

print("Found", len(pet_items), "pet(s), filtering...")
for pet_item in pet_items:
    pet_title = pet_item.text
    if "猫" not in pet_title:
        pet_link = (
            pet_item.find_element_by_class_name("item-listing-container")
            .find_element_by_tag_name("a")
            .get_attribute("href")
        )
        unfiltered_links.append(pet_link)

for link in unfiltered_links:
    browser.get(link)
    time.sleep(1)
    pet_summary = browser.find_element_by_class_name("details-section")
    if "wechat" not in pet_summary.text.lower():
        print("-----------------------------------------------------")
        print(pet_summary.text.split("\n")[0])
        print("")
        print(pet_summary.text.split("\n")[1])
        pet_details = browser.find_element_by_id("sidebar-reviews-pro").text.split("\n")
        pet_details = [x for x in pet_details if x]
        pprint(pet_details)
        print(link)
        print("-----------------------------------------------------")

print("Success")
