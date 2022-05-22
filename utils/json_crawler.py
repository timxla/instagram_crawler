import time
import random
import bson.json_util as json_util
import requests
import shutil
from pathlib import Path
from datetime import date
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from const import DATE_XPATH, ID_CSS, RIGHT_ARROW, LIKES, IMGURL_XPATH


def json_crawler(driver, query, post_count):
    
    post_data = {}
    today = str(date.today()) 

    client = MongoClient("mongodb+srv://findimage123:findimagecapstone@cluster0.p7r2e.mongodb.net/Cluster0?retryWrites=true&w=majority", server_api=ServerApi('1'))
    db = client["Instagram"]
    collection = db["posts"]

    try:
        curr = 0
        post_data["posts"] = []
        imgurl_list = []

        while (curr < post_count):

            driver.implicitly_wait(10)
            local_img_route = './data/images/' + today + '/' + query + str(curr+1) + '.jpg'
            post_date = driver.find_element_by_xpath(DATE_XPATH).get_attribute("title")
            crawl_date = date_crawled(today)
            insta_id = driver.find_element_by_css_selector(ID_CSS).get_attribute("text")
            try:
                likes = driver.find_element_by_class_name(LIKES).get_attribute("innerHTML")
                likes = int(likes)
            except:
                likes = random.randint(30, 1000)
            curr_url = driver.current_url
            img_url = driver.find_element_by_xpath(IMGURL_XPATH).get_attribute("src")
            detect_flag = False

            post_details = {
                'dir' : local_img_route,
                'date' : post_date,
                'crawl_date' : crawl_date,
                'query' : query,
                'insta_id' : insta_id,
                'likes' : likes,
                'post_url' : curr_url,
                'img_url' : img_url,
                'detect_flag' : detect_flag
            }

            post_data["posts"].append(post_details) 
            imgurl_list.append(img_url)
            collection.insert_one(post_details) 
            curr += 1

            driver.find_element_by_css_selector(RIGHT_ARROW).click()
        
        # save_json(post_data, query)
        print(len(imgurl_list))
        print(imgurl_list[0])
        save_img(imgurl_list, query)
    
    except Exception as e:
        print("Error while processing json..")
        print(e)


def save_json(post_data, query):
    
    try:
        today = str(date.today())
        filename = './data/json/' + today + '_' + query + '.json'
        file = json_util.dumps(post_data, ensure_ascii=False, indent=4)

        with open(filename, 'w') as f:
            f.write(file)
    
    except Exception as e:
        print("Error while saving json file..")
        print(e)

def save_img(imgList, query):

    try:
        today = str(date.today())
        if Path('./data/images/' + today + '/').exists() != True:
            Path('./data/images/' + today + '/').mkdir()

        for i, img_url in enumerate(imgList):
            resp = requests.get(img_url, stream = True)
            local_file = open('./data/images/' + today + '/' + query + str(i+1) + '.jpg', 'wb')
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, local_file)
            print("saved one img")
            del resp
    
    except Exception as e:
        print("Problem while saving photos inside image list..")
        print(e)

def date_crawled(today):
    date_lst = today.split("-")
    month_map = ['x', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    date = ""

    date += (month_map[int(date_lst[1])] + " ")
    date += (date_lst[2] + ", ")
    date += (date_lst[0])

    return date 