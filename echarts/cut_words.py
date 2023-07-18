import pymysql
import jieba.analyse

# 连接数据库
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


# jieba 分词加载自定义词库
# jieba.load_userdict("SogouLabDic.txt")
# jieba.load_userdict("dict_baidu_utf8.txt")
# jieba.load_userdict("dict_pangu.txt")
# jieba.load_userdict("dict_sougou_utf8.txt")
# jieba.load_userdict("dict_tencent_utf8.txt")
# jieba.load_userdict("my_dict.txt")

# 载入停止词
# stopwords = {}.fromkeys(
#      [line.rstrip() for line in open('Stopword.txt')])

# 从数据库中分别读取 ID1-ID9 的评论信息
sql = "select comment from books"
result = query(sql)
seg=[]
for item in result:
    result_middle=item
    # print(result_middle)
    a = jieba.lcut(result_middle[0])
    seg.extend(a)
result = []
# print(seg)
for i in seg:
            # if i not in stopwords:
    # print(i)
    result.append(i)
        # 将分好词的评论写入文件data_full.dat
    with open("data_full.dat", "a+", encoding="utf-8") as fo:
        fo.write(' '.join(i) + '\n')
        # 提取关键词并写入文件data_keywords.dat
    keywords = jieba.analyse.extract_tags(
            i, topK=30, withWeight=False,
            allowPOS=('ns', 'nr', 'nt', 'nz', 'nl', 'n', 'vn', 'vd', 'vg', 'v', 'vf', 'a', 'an', 'i'))
    with open("data_keywords.dat", "a+", encoding="utf-8") as fo:
            fo.write(' '.join(keywords) + '\n')
