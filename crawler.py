# Instagram Crawler
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from conf import INSTA_PASSWORD, INSTA_USERNAME
from const import LOGIN_URL, KEYWORDS, IMG_COUNT, SEARCH_XPATH, FIRST_POST, DRIVER_PATH
from utils.img_crawler import img_crawler, save_img
from utils.json_crawler import json_crawler

def make_chrome_driver(driver_path):
    driver = None

    try:
        driver = webdriver.Chrome(driver_path) 
    except:
        print("Problem when initiating driver.")

    return driver

def login(driver):
    flag = False
    driver.get(LOGIN_URL)
    time.sleep(5)

    try:
        username_el = driver.find_element_by_name('username')
        password_el = driver.find_element_by_name('password')

        username_el.send_keys(INSTA_USERNAME)
        password_el.send_keys(INSTA_PASSWORD)

        submit_btn_el = driver.find_element_by_css_selector("button[type='submit']")        
        submit_btn_el.click()
            
        time.sleep(4)    
        flag = True
        
    except:
        print("Error when logging in.")
        flag = False

    return flag

def search(driver, query):
    flag = False

    try:
        searchbox_el = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, SEARCH_XPATH)))
        searchbox_el.clear()

        searchbox_el.send_keys(query)

        time.sleep(3)
        searchbox_el.send_keys(Keys.ENTER)
        time.sleep(5)
        searchbox_el.send_keys(Keys.ENTER)
        time.sleep(5)
        flag = True

    except:
        print("Search failed")
        flag = False
    
    return flag 

def first_img_click(driver):
    flag = False

    try:
        time.sleep(3)
        driver.find_element_by_css_selector(FIRST_POST).click()
        flag = True
    
    except:
        print("An error occurred while clicking a post.")
        flag = False
    
    return flag

def scroll_to_top(driver):
    driver.find_element_by_tag_name('body').send_keys(Keys.HOME);
    time.sleep(5)


def crawler():
    is_login_success = False 
    driver = make_chrome_driver(DRIVER_PATH)

    if driver is not None:
        is_login_success = login(driver)

    if is_login_success:
        # KEYWORDS = ["#query1", "#query2"...]
        for query in KEYWORDS:
            is_search_success, is_first_img_click_success = False, False
            is_search_success = search(driver, query)

            # Image crawler
            if is_search_success:
                imgList = img_crawler(driver, IMG_COUNT)
                save_img(imgList, query)
            scroll_to_top(driver)

            # Metadata crawler
            is_first_img_click_success = first_img_click(driver)
            if is_first_img_click_success:
                json_crawler(driver, query, IMG_COUNT)

    print("Crawling completed.")
    print("Quitting driver..")
    driver.quit()


if __name__ == '__main__':
    crawler()
