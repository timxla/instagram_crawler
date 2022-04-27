from datetime import date
import shutil
import time
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from const import IMG_CSS, SCROLL_SCRIPT

def img_crawler(driver, post_count):
    
    try:
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        imgList = []

        while(len(imgList) <= post_count):
            posts = soup.select(IMG_CSS)
            for post in posts:
                imgUrl = post.select_one('.KL4Bh').img['src']
                imgList.append(imgUrl)
                imgList = list(set(imgList))

            driver.execute_script(SCROLL_SCRIPT)
            time.sleep(2)
            driver.execute_script(SCROLL_SCRIPT)
            time.sleep(2)
            driver.execute_script(SCROLL_SCRIPT)
            time.sleep(2)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")        
        
        imgList = imgList[:post_count]
        return imgList
    except Exception as e :
        print("Problem while scraping photots and saving to image list..")
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
            del resp
    
    except Exception as e:
        print("Problem while saving photos inside image list..")
        print(e)