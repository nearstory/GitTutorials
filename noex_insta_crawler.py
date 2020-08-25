from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
from selenium.common.exceptions import NoSuchElementException
import urllib.request


def crawl_insta(target):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    driver.get("https://www.instagram.com/" + target)
    driver.implicitly_wait(3)
    SPT = 1.0
    links = []
    prvt_set = set()

    while True:
        html = driver.page_source
        bsObj = BeautifulSoup(html, "lxml")
        for end_of_address in bsObj.select('.v1Nh3.kIKUG._bz0w a'):
            if end_of_address not in prvt_set:
                prvt_set.add(end_of_address)
                link = end_of_address.attrs['href']
                links.append(link)

        last_height = driver.execute_script(
            "return document.body.scrollHeight")
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SPT)
        new_height = driver.execute_script(
            "return document.body.scrollHeight")
        if new_height == last_height:
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SPT)
            new_height = driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            else:
                last_height = new_height
                time.sleep(0.3)
                continue

    temp_img = []
    temp_vid = []
    temp_picdate = []
    temp_viddate = []
    prvt_set2 = set()
    for i in links:
        url = 'https://www.instagram.com'+str(i)
        driver.get(url)
        time.sleep(0.3)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        while(1):
            try:

                if soup.select('video') not in soup:
                    pic_src = soup.select('.FFVAD')
                    pic_date = soup.select('time._1o9PC.Nzb55')
                    for i in pic_src:
                        if i not in prvt_set2:
                            prvt_set2.add(i)
                            temp_img.append(i.attrs['src'])
                            temp_picdate.append(pic_date[0].attrs['title'])

                if soup.select('video')[0] in soup.select('video'):
                    vid_src = soup.select('video')
                    vid_date = soup.select('time._1o9PC.Nzb55')
                    for g in vid_src:
                        if g not in prvt_set2:
                            prvt_set2.add(g)
                            temp_vid.append(g.attrs['src'])
                            temp_viddate.append(vid_date[0].attrs['title'])

                try:
                    driver.find_element_by_class_name(
                        "coreSpriteRightChevron").click()

                except NoSuchElementException:
                    break
            except:
                break

    if os.path.exists(target):
        os.rmdir(target)
    else:
        os.mkdir(target)

    num = 0
    for i in temp_img:
        urllib.request.urlretrieve(
            i, target+'/'+str(num)+"_"+temp_picdate[num]+"_"+target+'.png')
        num += 1

    num = 0
    for g in temp_vid:
        urllib.request.urlretrieve(
            g, target+'/'+str(num)+"_"+temp_viddate[num]+"_"+target+'.mp4')
        num += 1
    # # path = target
    # # path = os.path.realpath(path)
    # # os.system(path)

    driver.close()


while(1):
    a = input("사진 및 동영상을 다운받으실 계정명을 입력해주세요. : ")
    print("계정명이 " + a + "가 맞습니까?")
    print("맞으면 y, 틀리면 아무키나 눌러주세요.")
    b = input()
    if (b == "y" or b == "Y"):
        print("다운로드를 시작합니다. 데이터 양에 따라 5분 이상 소요될 수 있습니다.")
        break
    else:
        print("처음으로 되돌아갑니다.")
        continue
# 순환참조하는 방법?
crawl_insta(a)
