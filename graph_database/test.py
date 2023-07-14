from Bot import Bot
from queue import Queue
import pymysql
from py2neo import Graph
#爬取排行前10书籍的关系网
db_config = {"host": 'neo4j://localhost:7687', "user": 'neo4j', "password": '12345678'}

graph = Graph("neo4j://localhost:7687", auth = ('neo4j', '12345678'))

task_queue1 = Queue(maxsize = 100)
robot1 = Bot(task_queue1, db_config)
robot1.db_connection.clear_db()

con = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='123456',
    db='doubanbook',
    charset='utf8'
)

cur = con.cursor()
sql = "select link,title from books order by people desc limit 10"
cur.execute(sql)
results = cur.fetchall()

for result in results:
    task_queue1.put(int(''.join(filter(str.isdigit, result[0]))))
    robot1.run()
    print('任务队列大小',robot1.task_queue1.qsize())
    robot1.task_queue1.queue.clear()

    print('------------------------《',result[1],'》相关书籍爬取完毕-----------------------------')
    print('任务队列大小',robot1.task_queue1.qsize())

robot1.fill_books_info()
print("所有书籍爬取完毕")
cur.close()

#robot1.enqueue_boundary_books()
