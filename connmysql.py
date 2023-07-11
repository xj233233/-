from sqlalchemy.dialects.mysql import pymysql


def test1(table_name, data):
	## Release['MysqlIpOut']['HOST']：需要在__init__.py中定义好，写上后会提示需要导入
    dbIP = pymysql.connect['MysqlIpOut']['HOST']
    # 连接数据库
    mysql_connect = pymysql.connect(host=dbIP,
                                    user=pymysql.connect['Mysql']['username'],
                                    password=pymysql.connect['Mysql']['password'],
                                    database=pymysql.connect['Mysql']['dbName'],
                                    charset="utf8",
                                    port=3306,
                                    cursorclass=pymysql.cursors.DictCursor)
    cursor = mysql_connect.cursor()
    # 查询语句
    sql = "SELECT" + data + "FROM `" + table_name + "`"
    try:
    	# 执行sql语句
        cursor.execute(sql)
        # 提交更改为稳定存储
        mysql_connect.commit()
        # fetchall：获取所有行
        results = cursor.fetchall()
    except:
        results = {'code': '102'}
    finally:
    # 关闭连接
        mysql_connect.close()
    return results