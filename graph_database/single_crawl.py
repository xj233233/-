import re
from time import sleep
import requests
from bs4 import BeautifulSoup
from proxies import proxy


class Task2:
    def __init__(self, book_info, books_rec_ids, books_rec_names):
        self.book_info = book_info
        self.books_rec_ids = books_rec_ids
        self.books_rec_names = books_rec_names


# 单个页面的爬取
# 这里book_id是指书的id号
# 例如:https://book.douban.com/subject/1007305/ id就是1007305
def crawl_doubanbook_single_page(book_id):
    url = "https://book.douban.com/subject/" + str(book_id)
    headers = {
        'User-Agent': 'Mozilla/4.0 (Windows NT 6.1;WOW64) AppleWebKit/557.36 (KHTML,like GeCKO)\
                Chrome/45.0.2354.85 Safari/537.36 115Broswer/6.0.3',
        'Connection': 'keep-alive'}
    # 代理 在requests.get()中添加
    proxy_url = "https://dps.kdlapi.com/api/getdps/?secret_id=ocnh65ykq2w3ukhqjv8l&num=1&signature=a2crsngnfp1vpc533fuocy9805nrckfg&pt=2&sep=1"
    proxies = proxy(proxy_url)
    req_html = requests.get(url, headers=headers)
    req_html.encoding = req_html.apparent_encoding
    for i in range(5):
        try:
            if req_html.status_code == 200:
                print('成功获取源代码')
                break
        except Exception as e:
            print('状态码:', req_html.status_code, ' 获取源代码失败:' + e)
            print('再次请求')
        req_html = requests.get(url, headers=headers)
        req_html.encoding = req_html.apparent_encoding
        sleep(3)
        
    sleep(3)
    bsobj = BeautifulSoup(req_html.content, features="lxml")
    char_to_remove = ["\n", " ", "\xa0"]
    b_info = dict()
    # 这里有错误
    # ----------------本书信息----------------------------------------
    # ----------------书名-------------------------------------------
    b_name = bsobj.findAll("span", {"property": "v:itemreviewed"})[0].get_text()
    b_info["name"] = b_name

    # ----------------其它信息---------------------------------------
    b_info_wrap = bsobj.findAll("div", {"class": "subjectwrap clearfix"})
    b_info_tag = b_info_wrap[0].findAll("div", {"id": "info"})
    b_info_raw = b_info_tag[0].get_text()

    b_info["bid"] = book_id
    b_info_raw = str.replace(b_info_raw, " ", "")
    b_info_frag = b_info_raw.split("\n")

    for i in range(0, len(b_info_frag)):
        frag = b_info_frag[i]
        data0 = re.search(r"作者:", frag)
        data1 = re.search(r"出版社:(?P<Pub>\D*)", frag, re.M)
        data2 = re.search(r"ISBN:(?P<ISBN>\d*)", frag)
        data3 = re.search(r"页数:(?P<pages>\d*)", frag)
        data4 = re.search(r"出版年:(?P<pub_year>\d*)-(?P<pub_mon>\d*)", frag)
        data5 = re.search(r"丛书:(?P<collections>\D*)", frag)
        if data0 is not None:
            author_text = ""
            for j in range(i + 2, len(b_info_frag)):
                if re.search(r"出版社:(?P<Pub>\D*)", b_info_frag[j]) is not None:
                    break
                author_text += b_info_frag[j]
            author_list = author_text.split("/")
            b_info["authors"] = author_list
        if data1 is not None:
            b_info["publisher"] = data1.groupdict()["Pub"]
            # print(data1.groupdict()["Pub"])
        if data2 is not None:
            b_info["ISBN"] = str(data2.groupdict()["ISBN"])
        if data3 is not None:
            b_info["pages"] = data3.groupdict()["pages"]
        if data4 is not None:
            b_info["pub_year"] = data4.groupdict()["pub_year"]
            b_info["pub_mon"] = data4.groupdict()["pub_mon"]
            pass
        if data5 is not None:
            collection_name = data5.groupdict()["collections"]
            for bchar in char_to_remove:
                collection_name = str.replace(collection_name, bchar, "")
            b_info["collections"] = collection_name
        pass

    # ----------------评分-------------------------------------------
    b_rating_tag = b_info_wrap[0].findAll("strong", {"class": "ll rating_num"})
    if b_rating_tag[0].get_text() == ' ':  # 评分人数不足
        rating = -1
    else:
        rating = float(b_rating_tag[0].get_text())
    b_info["rating"] = rating
    # ----------------评分人数-------------------------------------------
    rating_people_tag = b_info_wrap[0].findAll("a", {"class": "rating_people"})
    if len(rating_people_tag) > 0:
        rating_people = rating_people_tag[0].get_text()
        rating_people_num = int(str.split(rating_people, '人')[0])
    else:
        rating_people_num = -1

    # ----------------本书相关推荐信息----------------------------------------------
    b_rec_lists = bsobj.findAll("div", {"class": "content clearfix"})
    if len(b_rec_lists) > 1:
        b_rec_list_dz = b_rec_lists[0].findAll("dl")  # 有电子书推荐条目
        b_rec_list = b_rec_lists[1].findAll("dl")
    elif len(b_rec_lists) == 1:
        b_rec_list = b_rec_lists[0].findAll("dl")  # 没电子书推荐条目

    b_rec_name_list = []
    b_rec_id_list = []

    for item in b_rec_list:
        name_text = item.get_text()
        for char in char_to_remove:
            name_text = str.replace(name_text, char, "")
        if name_text != "":
            b_rec_name_list.append(name_text)
            href = item.dt.a["href"]
            temp = str.split(href, "/")
            b_rec_id_list.append(temp[len(temp) - 2])

    task2_temp = Task2(b_info, b_rec_id_list, b_rec_name_list)
    print("《{0}》页面爬取完毕".format(b_info["name"]))
    return task2_temp
