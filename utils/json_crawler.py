import time
import json
from pathlib import Path
from datetime import date
from const import DATE_XPATH, ID_CSS, RIGHT_ARROW


def json_crawler(driver, query, post_count):
    
    post_data = {}

    try:
        today = str(date.today())
        curr = 0

        post_data[query] = []

        while (curr <= post_count):

            time.sleep(3)
            img_route = './data/images/' + today + '/' + query + str(curr+1) + '.jpg'
            post_date = driver.find_element_by_xpath(DATE_XPATH).get_attribute("title")
            post_id = driver.find_element_by_css_selector(ID_CSS).get_attribute("text")

            post_details = {
                'dir' : img_route,
                'date' : post_date,
                'id' : post_id
            }
        
            post_data[query].append(post_details) 
            curr += 1

            driver.find_element_by_css_selector(RIGHT_ARROW).click()
        
        save_json(post_data, query)
    
    except Exception as e:
        print("Error while processing json..")
        print(e)


def save_json(post_data, query):
    
    try:
        today = str(date.today())
        filename = './data/json/' + today + '_' + query + '.json'

        with open(filename, 'w+') as f:
            json.dump(post_data, f, indent=2, ensure_ascii=False)
    
    except Exception as e:
        print("Error while saving json file..")
        print(e)