import requests


def zdaye():
    url = "http://www.zdopen.com/PrivateProxy/GetIP/?api=202009122220574726&akey=11e39a376e9bff94&fitter=2&timespan=15&tunnel=1&type=3"

    r = requests.get(url).json()

    return r

def ck_ip(proxies):
    url = "http://icanhazip.com/"

    txt = requests.get(url,proxies=proxies).text
    print(txt)



def run():
    ad = zdaye()
    if ad['code'] != '10001':
        return None

    proxy_list = []

    for pl in ad['data']['proxy_list']:
        p = {
            'http':'http://{}:{}'.format(pl["ip"],pl["port"]),
            'https':'https://{}:{}'.format(pl["ip"],pl["port"]),
        }

        proxy_list.append(p)

    return proxy_list


if __name__ == '__main__':
    p = run()[0]
    ck_ip(p)
    print(p)
