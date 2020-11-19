import requests
from faker import Faker
import execjs
import os

fake = Faker()


class BaiduFanyi(object):

    def __init__(self):
        self.url = "https://fanyi.baidu.com/v2transapi"


    def fanyi(self, q, f, t):

        headers = {
            "User-Agent": fake.user_agent(),
            "origin": "https://fanyi.baidu.com",
            "referer": "https://fanyi.baidu.com/",
        }

        params = {
            'from': f,
            'to': t
        }


        form_data = {
            "from": f,
            "to": t,
            "query": q,
            "transtype": "realtime",
            "simple_means_flag": "3",
            "sign": "594751.913422",
            "token": "998c463d951d282b340110fc700d2030",
            "domain": "common",
        }


        response = requests.post(self.url, headers=headers, params=params, data=form_data)

        print(response.text)


if __name__ == '__main__':
    baidfanyi = BaiduFanyi()

    # baidfanyi.fanyi("apple",'en','zh')

    with open(os.path.join(os.getcwd(), "script.txt"), 'r', encoding='utf-8') as f:
        comp = execjs.compile(f.read())

    comp.call("e","apply")  # 240425.477208
