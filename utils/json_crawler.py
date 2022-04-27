import time
import json
import bson.json_util as json_util
from pathlib import Path
from datetime import date
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from const import DATE_XPATH, ID_CSS, RIGHT_ARROW
from conf import INSTA_PASSWORD, INSTA_USERNAME


def json_crawler(driver, query, post_count):
    
    post_data = {}
    today = str(date.today())

    client = MongoClient("mongodb+srv://findimage123:findimagecapstone@findimage.qp8zm.mongodb.net/findimage?retryWrites=true&w=majority", server_api=ServerApi('1'))
    db = client[today]
    collection = db[query]

    try:
        curr = 0

        post_data[query] = []

        while (curr <= post_count):

            time.sleep(5)
            img_route = './data/images/' + today + '/' + query + str(curr+1) + '.jpg'
            post_date = driver.find_element_by_xpath(DATE_XPATH).get_attribute("title")
            post_id = driver.find_element_by_css_selector(ID_CSS).get_attribute("text")
            curr_url = driver.current_url

            post_details = {
                'dir' : img_route,
                'date' : post_date,
                'id' : post_id,
                'url' : curr_url,
            }

            post_data[query].append(post_details) 
            collection.insert_one(post_details) 
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
        file = json_util.dumps(post_data)

        with open(filename, 'w+') as f:
            json.dump(file, f, indent=2, ensure_ascii=False)
    
    except Exception as e:
        print("Error while saving json file..")
        print(e)
