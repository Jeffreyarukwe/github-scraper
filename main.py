from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from utils.helper import is_valid_url, validate_github_url
from utils.possible_secrets import possible_secrets

scrape = False
found_counter = 0

repo_url = input("Enter the GitHub URL you want to scrape: ")

if not is_valid_url(repo_url):
    print("Invalid URL")
else:
    if not validate_github_url(repo_url):
        print("Not a GitHub URL")
    else:
        scrape = True

chrome_driver_path = "/Users/Jeffr/Downloads/Development/chromedriver"
driver = webdriver.Chrome()

while scrape:

    driver.get(repo_url)

    repositories = driver.find_elements(By.CLASS_NAME, 'repo')

    links = []
    new_links = []

    def find_raw(page):
        global found_counter
        driver.get(page)
        try:
            raw_page = driver.find_element(By.XPATH,
                                           '//*[@id="repos-sticky-header"]/div[1]/div[2]/div[2]/div[1]/div[1]/a')
            raw_page.click()

            html = driver.page_source
            html = f"{html}"

            for secret_word in possible_secrets:
                if secret_word in html:
                    found_counter += 1
                    print(f"Found '{secret_word}' in: {page}")

        except Exception as e:
            print(f"Error finding raw page on {page}: {e}")

    def traverse_first_page(page):
        driver.get(page)
        time.sleep(2)

        files_to_check = driver.find_elements(By.CLASS_NAME, 'Link--primary')
        second_links = []

        for file in files_to_check:
            if ".py" in file.text or ".ipynb" in file.text or ".js" in file.text:
                second_links.append(file.text)

        for link2 in second_links:
            new_page = f"{page}/blob/master/{link2}"
            find_raw(new_page)

    for repo in repositories:
        links.append(repo.text)

    for link in links:
        next_page = f"{repo_url}/{link}"
        traverse_first_page(next_page)

    if found_counter == 0:
        print("None found ✅")

    scrape = False

driver.quit()
