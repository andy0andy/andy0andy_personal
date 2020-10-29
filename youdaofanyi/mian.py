import requests
import time
import random
import hashlib




def r(e):
    appVersion = "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"


    t = hashlib.md5(appVersion.encode('utf-8')).hexdigest()

    r = str(int(time.time() * 1000))

    i = r + str(random.randint(0,9))

    sign = hashlib.md5(("fanyideskweb" + e + i + "]BjuETDhU)zqSxf-=B#7m").encode('utf-8')).hexdigest()

    return {
        'lts':r,
        'bv':t,
        'salt':i,
        'sign':sign
    }



def fanyi(word):
    url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"

    headers = {
        "Referer":"http://fanyi.youdao.com/",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
        "Cookie":"OUTFOX_SEARCH_USER_ID=1892099298@10.169.0.82; OUTFOX_SEARCH_USER_ID_NCOO=177514885.45283633; _ntes_nnid=232683c6a5b072dd7073fafc1ee2be7c,1584941323856; _ga=GA1.2.1141603924.1585885862; JSESSIONID=aaaCwP56Wzqj788eakgsx; ___rl__test__cookies=1599984053765",
    }


    data = r(word)

    form_data = {
        "i": word,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",

        "salt": data['salt'],
        "sign": data['sign'],
        "lts": data['lts'],
        "bv": data['bv'],

        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTlME",
    }



    response = requests.post(url,data=form_data,headers=headers)

    res = response.json()

    return res



if __name__ == '__main__':
    res = fanyi('apple')

    print(res)


