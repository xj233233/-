import os

from flask import render_template
from pyecharts import options as opts
from pyecharts.charts import Map
import pymysql
from pyecharts.faker import Faker
def get_conn():
    """
    :return 连接对象，游标对象
    """
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        passwd="111111",
        db="doubanbook",
        charset="utf8"
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

country = []
num = []
sql = "select * from book_country_num"
result = query(sql)
for item in result:
    country.append(str(item[0]))
    num.append(item[1])
print(num)

# 基础数据
value = [131, 1, 3, 1, 1, 1, 2, 3, 3, 5, 1, 8, 1, 1, 15, 1, 5, 1, 1, 1, 1, 2, 33, 1, 1, 23, 1, 1]
attr = ["China", "Israel", "Russia", "Canada", "South Africa", "India", "Ancient Greece", "Colombia", "Austria", "Germany", "Germany", "Italy", "Norway", "Japan", "Japan", "France", "Qing", "Australia", "Sweden", "White Russia", "United States","Soviet","Britain","Portugal","Argentina"]

data = []
for index in range(len(attr)):
    city_ionfo = [attr[index], value[index]]
    data.append(city_ionfo)

c = (
    Map()
    .add("世界地图", data, "world")
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="对应国家地图示例"),
        visualmap_opts=opts.VisualMapOpts(max_=200),

    )
    .render()
)

# 打开html
# os.system("templates/render.html")

