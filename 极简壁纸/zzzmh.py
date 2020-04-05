import requests
import json
import time


# 返回一页的 Json数据
def get_one_page(pageNum,target):
    data = {
        'pageNum': pageNum,
        'target': target
    }

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "access": "b9abb5db9f95e0439fe7d885123696e907d1352c3909ab0035a346168cfc5679",
        "content-length": "30",
        "location": "bz.zzzmh.cn",
        "origin": "https://bz.zzzmh.cn",
        "referer": "https://bz.zzzmh.cn/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sign": "f566907d5b5fc72aa0d9df9674cfcebf",
        "timestamp": "1585403003757",
        'Content-Type': 'application/json',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }


    url = "https://api.zzzmh.cn/bz/getJson"


    response = requests.post(url,data=json.dumps(data),headers=headers,verify=False)

    # print(response.json())
    return response.json()

# 获取一页壁纸的url地址
def get_img_url(jsons):
    pub_url = "https://th.wallhaven.cc/small/"

    records = jsons['result']['records']

    for recode in records:
        img_url = pub_url + r"/" + recode['i'][:2] + r'/' + recode['i'] + ".jpg"

        yield {
            'img_url':img_url,
            'title':recode['i']
        }

# 下载壁纸
def write_img(item):
    with open("static/{}.jpg".format(item['title']),'wb') as f:
        img = requests.get(item['img_url'])
        f.write(img.content)

        print("{} ok".format(item['title']))


def main():
    jsons = get_one_page("1","index")
    for item in get_img_url(jsons):
        # 延时操作，一张图片停半秒
        time.sleep(0.5)
        write_img(item)


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()

    print("用时：",end-start)
    print("OK!")