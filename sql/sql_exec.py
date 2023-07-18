import pymysql
#database:数据库名称
#sql:sql文件的路径
def execute_sql(database:str , sql: str):
    sql_item = ''
    try:
        #请修改为自己的数据库连接
        db = pymysql.connect(
            host="123.249.31.143",
            user="test001",
            password="P@ssw0rd",
        )
        print("连接成功")
        conn = db.cursor()
        conn.execute("CREATE DATABASE IF NOT EXISTS `%s`;" % database)
    except Exception as e:
        print(e + "连接失败")

    try:
        # 请修改为自己的数据库连接
        db = pymysql.connect(
            host= "123.249.31.143",
            user= "test001",
            password="P@ssw0rd",
            database = database
        )
        connector = db.cursor()
        with open(sql, encoding='utf-8', mode='r') as f:
            # 读取整个sql文件，以分号切割。[:-1]删除最后一个元素，也就是空字符串
            sql_list = f.read().split(';')[:-1]
            for x in sql_list:
                # 判断包含空行的
                if '\n' in x:
                    # 替换空行为1个空格
                    x = x.replace('\n', ' ')

                # 判断多个空格时
                if '    ' in x:
                    # 替换为空
                    x = x.replace('    ', '')

                # sql语句添加分号结尾
                sql_item = x + ';'
                connector.execute(sql_item)
                db.commit()
                print("执行成功sql: %s" % sql_item)
            connector.close()

    except Exception as e:
        print(e)
        print('执行失败sql: %s' % sql_item)

def list_insert(list):
    # 请修改为自己的数据库连接
    execute_sql("doubanbook", "sql/create_doubanbook.sql")
    db = pymysql.connect(
        host="123.249.31.143",
        user="test001",
        password="P@ssw0rd",
        database="doubanbook"
    )

    conn = db.cursor()

    book_list = list
    # 字典数据
    # 列字段
    keys = "  title, \
              link, \
              country,\
              author, \
              translator, \
              publisher, \
              press_time,\
              price, \
              star,\
              score, \
              people, \
              comment "

    for book_elemnets in book_list:
        table = "books"
        # 行字段
        values = ', '.join(['%s'] * len(book_elemnets))
        sql = 'REPLACE INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
        # 将字段的value转化为元组存入

        try:
            # 这里的第二个参数传入的要是一个元组
            if conn.execute(sql, tuple(book_elemnets.values())):
                db.commit()
        except Exception as  e:
            print('Insert Failed: %s ' % e)
            db.rollback()

    conn.close()

    execute_sql("doubanbook", "sql/create_doubanbook.sql")
