from Cloud import Cloud


def pretty_songs(songs):
    ids = []

    print("{0: ^10}{1: <30}{2: <30}{3: <30}\n".format('ID','音乐标题','歌手','专辑'))
    print('-'*100)

    for i,s in enumerate(songs):
        name = s['name'].strip()
        ar = s['ar'].strip()
        al = s['al'].strip()
        if len(name) > 20:
            name = s['name'][:15]
        elif len(s['ar']) > 20:
            ar = s['ar'][:15]
        elif len(s['al']) > 20:
            al = s['al'][:15]

        print("{0: ^10}{1: <30}{2: <30}{3: <30}\n".format(i, name, ar, al))

        ids.append(s['id'])

    return ids



def run():
    cloud = Cloud()

    flag = True

    while flag:
        word = input("请输入搜索词...\n")

        songs = cloud.search(word)

        ids = pretty_songs(songs)

        yn = input("是否需要下载（y/n）\n")

        if yn == "y":

            dl = True

            while dl:

                index = int(input("请选择下载歌曲(输入id即可)\n"))

                try:
                    music_file = f"{ids[index]}.mp3"
                    cloud.download_music(ids[index],music_file)

                    yn = input("是否下载歌词（y/n）\n")

                    if yn == 'y':
                        words_file = f"{ids[index]}.txt"
                        cloud.download_words(ids[index],words_file)
                except:
                    print('输入错误')

                yn = input("是否继续下载（y/n）\n")

                if yn == "n":
                    dl = False


        # 结束
        yn = input('是否结束程序（y/n）\n')
        if yn == 'y':
            flag = False


if __name__ == '__main__':

    run()


