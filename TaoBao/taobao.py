from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from pyquery import PyQuery as pq
import json

class Taobao():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'")
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])

        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.maximize_window()

        self.driver.implicitly_wait(10)

    def tlogin(self):
        url = "https://login.taobao.com/member/login.jhtml"
        self.driver.get(url)

        WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.ID,"J_SubmitStatic")))

        try:
            action = ActionChains(self.driver)
            login_switch = self.driver.find_element(By.CLASS_NAME,"login-switch")
            x = login_switch.location['x'] + login_switch.size['width']
            y = login_switch.location['y']

            action.move_by_offset(x,y).click()

            action.perform()
        except:
            pass


    def search_goods(self,goods):
        while True:
            if self.driver.find_element(By.ID, "q"):
                break

        self.driver.find_element(By.ID,'q').send_keys(goods)
        time.sleep(random.randint(0,1))
        self.driver.find_element(By.CLASS_NAME,"tb-bg").click()

        WebDriverWait(self.driver, 8).until(EC.presence_of_element_located((By.CLASS_NAME, "items")))

        doc = pq(self.driver.page_source)
        items = doc("#J_itemlistCont").prev()
        item = items(".J_MouserOnverReq")
        for i in item.items():

            # print("图片：", i(".J_ItemPic").attr("data-src"))
            # print("价格：", i(".price strong").text())
            # print("标题：", i("a.J_ClickStat").text())
            # print("商铺：", i(".dsrs").next().text())
            # print("地址：", i(".location").text())
            # print("购买人数：", i(".deal-cnt").text())
            # print("------------------")

            yield {
                "图片：":i(".J_ItemPic").attr("data-src"),
                "价格：": i(".price strong").text(),
                "标题：":i("a.J_ClickStat").text(),
                "商铺：": i(".dsrs").next().text(),
                "地址：": i(".location").text(),
                "购买人数：": i(".deal-cnt").text()
            }

    def write_json(self,f,item):
        f.write(json.dumps(item,ensure_ascii=False) + '\n')


def main():
    f = open("taobao.json","a",encoding='utf-8')
    taobao = Taobao()
    taobao.tlogin()
    for item in taobao.search_goods("python爬虫"):
        taobao.write_json(f,item)

    f.close()

    taobao.driver.quit()


if __name__ == '__main__':

    main()

    print("OK!!!")