import requests
from flask import Flask, render_template, request, redirect, url_for
import pymysql
import json
from graph_database import Bot
from queue import Queue
from py2neo import Graph

app = Flask(__name__)


def get_conn():
    """
    :return 连接对象，游标对象
    """
    conn = pymysql.connect(
        host='123.249.31.143',
        port=3306,
        user='test001',
        passwd='P@ssw0rd',
        db='doubanbook',
        charset='utf8'
    )
    # 创建游标
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def query(sql, *args):
    """
    通用查询
    :param sql
    :param args sql里的占位符对应的值
    :return 返回查询的结果， ((),()...)
    """
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/index')
def home():
    # return render_template("index.html")
    return index()


@app.route('/book')
def tushu():
    datalist = []
    sql = "select * from books"
    result = query(sql)
    for item in result:
        datalist.append(item)
    return render_template("book.html", book=datalist)


# 检索
@app.route('/search', methods=['POST'])
def search():
    find_book = []
    keywords = request.form.get('keywords')
    # sql = "select * from books where title like '%" + keywords + "%' "
    sql = 'select * from books where title like "%%{0}%%"'.format(keywords)
    result = query(sql)
    for item in result:
        find_book.append(item)
    return render_template('book.html', book=find_book)


@app.route('/score')
def score():
    score = []  # 评分
    num = []  # 每个评分所统计出的电影数量
    sql = "select * from book_score_num"
    result = query(sql)
    for item in result:
        score.append(str(item[0]))
        num.append(item[1])

    return render_template("score.html", score=score, num=num)


@app.route('/country')
def country():
    country = []  # 评分
    num = []  # 每个评分所统计出的电影数量
    sql = "select * from book_country_num"
    result = query(sql)
    for item in result:
        country.append(str(item[0]))
        num.append(item[1])

    return render_template("country.html", country=country, num=num)


@app.route('/country_map')
def country_map():
    return render_template("country_map.html")


@app.route('/peopletop10')
def peopletop10():
    people = []  # 评论人数
    title = []  # 书名
    s = []
    sql = "select * from book_people_title"
    result = query(sql)
    for item in result:
        s.append(item)
        people.append(str(item[0]))
        title.append(item[1])

    return render_template("peopletop10.html", people=people, title=title)


@app.route('/presstime')
def presstime():
    year = []
    num = []
    s = []
    sql = "select * from book_presstime_num"
    result = query(sql)
    for item in result:
        s.append(item)
        year.append(str(item[0]))
        num.append(item[1])

    return render_template("presstime.html", year=year, num=num)


@app.route('/publisher')
def publisher():
    year = []
    num = []
    s = []
    sql = "select * from book_publisher_num"
    result = query(sql)
    for item in result:
        s.append(item)
        year.append(str(item[0]))
        num.append(item[1])

    return render_template("publisher.html", year=year, num=num)


def push_to_gData(gData, unique_nodes, cur):
    links = gData["links"]
    nodes = gData["nodes"]

    for data in cur:
        source_node = data[0]
        target_node = data[1]
        if source_node["bid"] not in unique_nodes:
            unique_nodes[source_node["bid"]] = dict(source_node)
            nodes.append({"id": source_node["bid"], "book_data": dict(source_node), "rating": source_node["rating"]})
        if target_node["bid"] not in unique_nodes:
            unique_nodes[target_node["bid"]] = dict(target_node)
            nodes.append({"id": target_node["bid"], "book_data": dict(target_node), "rating": source_node["rating"]})

        link_obj = {"source": source_node["bid"], "target": target_node["bid"]}
        links.append(link_obj)

    gData = {"nodes": nodes, "links": links}
    return gData, unique_nodes


@app.route('/rel', methods=['POST', 'GET'])
def book_connection_query_rand():
    graph = Graph("neo4j://localhost:7687", auth=("neo4j", "12345678"))
    gData = {"nodes": [], "links": []}
    result = request.form.get("bid")
    bid = ''.join(filter(str.isdigit, str(result)))
    print(bid)
    if request.method == 'POST':
        cur = graph.run("MATCH (m:{0}) <-[:读者可能喜欢]-(p) RETURN * ".format("favor" + bid))
    else:
        cur = graph.run("MATCH (m) <-[:读者可能喜欢]-(p) RETURN * limit 200")

    cur_data = [item for item in cur]
    gData, unique_nodes = push_to_gData(gData, {}, cur_data)

    return render_template('3d-force-graph.html', gData=json.dumps(gData))



@app.route('/wordcloud_custom_mask_image')
def word():
    return render_template("wordcloud_custom_mask_image.html")


@app.route('/team')
def team():
    return render_template("team.html")


if __name__ == '__main__':
    from gevent import pywsgi

    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)

    server.serve_forever()
