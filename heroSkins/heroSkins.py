import requests
import os
import time

def get_hero_list(url):
    response = requests.get(url,headers=headers)
    response.encoding =response.apparent_encoding

    heros = response.json()

    for hero in heros['hero']:
        item = {}

        item['id'] = hero['heroId']
        item['name'] = '-'.join([hero['name'],hero['title']])

        yield item


def get_one_hero(item):
    hero_url = "https://game.gtimg.cn/images/lol/act/img/js/hero/" + item['id'] + ".js"

    response = requests.get(hero_url,headers=headers)
    response.encoding = response.apparent_encoding

    hero = response.json()

    os.mkdir(item['name'])
    for skin in hero['skins']:
        if skin['mainImg']:
            skin_file = "{}/{}.jpg".format(item['name'],skin['name'].replace('/',""))
            skin_img = requests.get(skin['mainImg'],headers=headers)

            with open(skin_file,'wb+') as f:
                f.write(skin_img.content)

    print(item['name'],'OK')


if __name__ == "__main__":

    url = "https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js"


    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
    }

    # get_one_hero({'id':'1',"name":"黑暗之女-安妮"})

    for item in get_hero_list(url):
        get_one_hero(item)

        time.sleep(1)

    print("OK")