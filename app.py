from flask import Flask, render_template
import pymysql
from pyecharts.charts import Map

app = Flask(__name__)

def get_conn():
    """
    :return 连接对象，游标对象
    """
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='yyp20020923',
        db='doubanbook',
        charset='utf8'
    )
    #创建游标
    cursor = conn.cursor()
    return conn,cursor

def close_conn(conn,cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def query(sql,*args):
    """
    通用查询
    :param sql
    :param args sql里的占位符对应的值
    :return 返回查询的结果， ((),()...)
    """
    conn,cursor = get_conn()
    cursor.execute(sql,args)
    res = cursor.fetchall()
    close_conn(conn,cursor)
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
    print(datalist)
    return render_template("book.html", book=datalist)


@app.route('/score')
def score():
    score = []
    num = []
    sql = "select * from book_score_num"
    result = query(sql)
    for item in result:
        score.append(str(item[0]))
        num.append(item[1])

    return render_template("score.html", score=score, num=num)


@app.route('/country')
def country():
    country = []
    num = []
    sql = "select * from book_country_num"
    result = query(sql)
    for item in result:
        country.append(str(item[0]))
        num.append(item[1])

    return render_template("country.html", country=country, num=num)


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


@app.route('/word')
def word():
    return render_template("word.html")


@app.route('/team')
def team():
    return render_template("team.html")

def render_country():
    # 基础数据
    value = [131, 1, 3, 1, 1, 1, 2, 3, 3, 5, 1, 8, 1, 1, 15, 1, 5, 1, 1, 1, 1, 2, 33, 1, 1, 23, 1, 1]
    attr = ["China", "Israel", "Russia", "Canada", "South Africa", "India", "Ancient Greece", "Colombia", "Austria",
            "Germany", "Germany", "Italy", "Norway", "Japan", "Japan", "France", "Qing", "Australia", "Sweden",
            "White Russia", "United States", "Soviet", "Britain", "Portugal", "Argentina"]

    data = []
    for index in range(len(attr)):
        city_ionfo = [attr[index], value[index]]
        data.append(city_ionfo)

    c = (
        Map()
        .add("世界地图", data, "world")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="作家对应国家地图示例"),
            visualmap_opts=opts.VisualMapOpts(max_=200),

        )
        .render("templates/country_map.html")
    )
    return render_template("country_map.html",country_list =data)


if __name__ == '__main__':
    from gevent import pywsgi
    #需要重新绘制时取消下面的注释，运行app(注意保留原map的"visualMap")
    # render_country()
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)

    server.serve_forever()

