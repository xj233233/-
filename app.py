from flask import Flask, render_template, request
import pymysql


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


@app.route('/wordcloud_custom_mask_image')
def tushu():
    datalist = []
    sql = "select * from books"
    result = query(sql)
    for item in result:
        datalist.append(item)
    print(datalist)
    return render_template("wordcloud_custom_mask_image.html", book=datalist)

# 检索
@app.route('/search', methods=['POST'])
def search():
    find_book = []
    keywords = request.form.get('keywords')
    print(keywords)
    # sql = "select * from books where title like '%" + keywords + "%' "
    sql = 'select * from books where title like "%%{0}%%"'.format(keywords)
    result = query(sql)
    for item in result:
        find_book.append(item)
    print(find_book)
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


@app.route('/word')
def word():
    return render_template("word.html")


@app.route('/team')
def team():
    return render_template("team.html")


if __name__ == '__main__':
    from gevent import pywsgi

    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)

    server.serve_forever()

