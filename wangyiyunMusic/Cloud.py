import requests
from fake_useragent import UserAgent
from Crypto.Cipher import AES
from  Crypto.Util.Padding import pad
import base64
import json
import random
import math
import execjs



class Cloud(object):

    ua = UserAgent()

    # 搜索接口
    search_url = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="

    # 下载音乐接口
    download_music_url = "http://music.163.com/song/media/outer/url?id={}"

    # 下载歌词接口
    download_words_url = "https://music.163.com/weapi/song/lyric?csrf_token="

    # 固定参数
    e = "010001"
    f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
    g = "0CoJUm6Qyw8W8jud"


    def change_d(self, word, type):

        if type == 'search':     # 搜索
            d = {
                "hlpretag" : r"<span class=\"s-fc7\">",
                "hlposttag" : r"</span>",
                "s" : word,
                "type" : "1",
                "offset" : "0",
                "total" : "true",
                "limit" : "30",
                "csrf_token" : ""}
        elif type == 'words':   # 下载歌词
            d = {
                "id" : word,
                "lv" : "-1",
                "tv" : "-1",
                "csrf_token" : "",
            }


        d = json.dumps(d,ensure_ascii=False)

        return d

    # AES加密，对应函数b
    def AESEncrypt(self, content, key):

        # 数据填充
        content = pad(data_to_pad=content.encode(), block_size=AES.block_size)

        key = key.encode('utf-8')
        iv = '0102030405060708'.encode('utf-8')

        aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
        cipher_text = aes.encrypt(plaintext=content)

        # 字节串转为字符串
        cipher_texts = base64.b64encode(cipher_text).decode('utf-8')

        return cipher_texts

    # 16位随机字符串， 对应函数a
    def function_a(self,l):
        b = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        c = ''

        for d in range(l):
            e = float(str(random.random())[:-1]) * len(b)
            e = math.floor(e)

            c += b[e]

        return c

    # 获得加密参数 params
    def params(self , i, d):

        res = self.AESEncrypt(d,self.g)
        res = self.AESEncrypt(res,i)


        return res

    # 获得加密参数 encSecKey
    def encSecKey(self,i):
        with open('c.txt', 'r') as f:
            js_c = f.read()

        comp = execjs.compile(js_c)

        res = comp.eval('c("{}","{}","{}")'.format(i, self.e, self.f))
        # print(res)

        return res


    # 搜索
    def search(self, word):
        i = self.function_a(16)

        d = self.change_d(word,'search')

        data = {
            'params' : self.params(i,d),
            'encSecKey' : self.encSecKey(i)
        }

        headers = {
            'User-Agent' : self.ua.random
        }

        r = requests.post(self.search_url, data=data, headers=headers).json()


        if r['code'] == 200:

            songs = []

            for s in r['result']['songs']:
                item = {}

                item['id'] = s['id']
                item['name'] = s['name']
                item['ar'] = '/'.join([ar['name'] for ar in s['ar']])
                item['al'] = s['al']['name']

                songs.append(item)

            return songs
        else:
            return None

    # 下载音乐
    def download_music(self,id,filename):

        headers = {
            'User-Agent': self.ua.random
        }

        r = requests.get(self.download_music_url.format(id), headers=headers).content

        with open(filename,'wb') as f:
            f.write(r)

        print("下载音乐成功...")

    # 下载歌词
    def download_words(self, id, filename):
        i = self.function_a(16)

        d = self.change_d(id, 'words')

        data = {
            'params': self.params(i, d),
            'encSecKey': self.encSecKey(i)
        }

        headers = {
            'User-Agent': self.ua.random
        }

        r = requests.post(self.download_words_url, data=data, headers=headers).json()

        if r['code'] == 200:
            lyric =  r['lrc']['lyric']

            with open(filename,'w',encoding='utf-8') as f:
                f.write(lyric)

            print("下载歌词成功...")

        else:
            return None


if __name__ == '__main__':
    cs = Cloud()

    # cs.search('芒种')

    # cs.download_music('1369798757','芒种.mp3')

    # cs.download_words('1369798757','芒种.txt')


