# Instagram Crawler
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from conf import INSTA_PASSWORD, INSTA_USERNAME
from const import LOGIN_URL, KEYWORDS, IMG_COUNT, FIRST_POST
from utils.img_crawler import img_crawler, save_img
from utils.json_crawler import json_crawler

def make_chrome_driver():
    driver = None

    try:
        driver = webdriver.Chrome(ChromeDriverManager().install()) 
    except Exception as e:
        print("Problem when initiating driver.")
        print(e)

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


# Need to click the first photo in order to target id, date
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

# After crawling img files, scroll to top to click on the first post
def scroll_to_top(driver):
    driver.find_element_by_tag_name('body').send_keys(Keys.HOME);
    time.sleep(5)



def crawler():
    is_login_success = False 
    driver = make_chrome_driver()
    time.sleep(5)

    if driver is not None:
        is_login_success = login(driver)

    if is_login_success:
        for query in KEYWORDS:
            is_first_img_click_success = False

            # Image crawler
            driver.get("https://instagram.com/explore/tags/" + query + "/")
            time.sleep(5)

            """
            To save images locally, uncomment the lines below
            """
            #imgList = img_crawler(driver, IMG_COUNT)
            #save_img(imgList, query)
            #scroll_to_top(driver)

            is_first_img_click_success = first_img_click(driver)
            if is_first_img_click_success:
                json_crawler(driver, query, IMG_COUNT)

    print("Crawling completed.")
    print("Quitting driver..")
    driver.quit()


if __name__ == '__main__':
    crawler()
