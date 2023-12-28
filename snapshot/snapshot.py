from selenium import webdriver
import time
import os
import shutil
import pymongo
from datetime import datetime
import threading

# 连接到 MongoDB
client = pymongo.MongoClient("localhost", 27017)
db = client["Newsina"]
collection = db["newsina"]

# 存储快照的目录
snapshot_dir = "./snapshot_img"


# 删除旧的快照目录（如果存在），然后创建一个新目录
# if os.path.exists(snapshot_dir):
#     shutil.rmtree(snapshot_dir)
# os.makedirs(snapshot_dir)

def webshot(url, saveImgName, total_page):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    try:
        driver.get(url)
        time.sleep(1)  # 等待页面初步加载

        # 获取页面总高度
        total_height = driver.execute_script("return document.body.parentNode.scrollHeight")

        # 循环滚动并截图
        for i in range(1, int(total_height / 500) + 2):
            driver.execute_script(f"window.scrollTo(0, {(i * 500)});")
            time.sleep(0.01)  # 稍微等待页面加载

        # 调整窗口捕获整个页面
        driver.set_window_size(driver.execute_script("return document.body.scrollWidth;"), total_height)
        driver.save_screenshot(os.path.join(snapshot_dir, f"{saveImgName}.png"))
        
        
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"Saved screenshot for {url} as {saveImgName}.png, {total_page}, {current_time}")
        total_page += 1
    except Exception as e:
        print(f"Error capturing {url}: {e}")
    finally:
        driver.quit()

def snapshot_thread(url, name, total_page):
    snapshot_path = os.path.join(snapshot_dir, f"{name}.png")
    if os.path.exists(snapshot_path):
        print(f"Snapshot for {name} already exists, skipping.", total_page)
    else:
        webshot(url, name, total_page)

if __name__ == '__main__':
    total_page = 0
    threads = []

    for document in collection.find():
        total_page += 1
        url = document.get("url")
        name = document.get("title")
        
        # 创建一个线程
        thread = threading.Thread(target=snapshot_thread, args=(url, name, total_page))
        threads.append(thread)
        thread.start()
            
        if len(threads) >= 8:  # 如果已经有两个线程在运行，等待它们完成
            for t in threads:
                t.join()
            threads = []  # 清空线程列表，准备下一轮

    # 等待最后一批线程完成
    for t in threads:
        t.join()