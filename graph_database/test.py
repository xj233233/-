from Bot import Bot
from queue import Queue
import pymysql
from py2neo import Graph
# 1007305
db_config = {"host": 'neo4j://localhost:7687', "user": 'neo4j', "password": '12345678'}

graph = Graph("neo4j://localhost:7687", auth = ('neo4j', '12345678'))



con = pymysql.connect(
    host='123.249.31.143',
    port=3306,
    user='test001',
    passwd='P@ssw0rd',
    db='doubanbook',
    charset='utf8'
)

cur = con.cursor()
sql = "select link from books"
cur.execute(sql)
results = cur.fetchall()

task_queue1 = Queue(maxsize = 100)

#robot1.db_connection.clear_db()
bids = []
for result in results:
    bids.append(int(''.join(filter(str.isdigit, str(result)))))


for i in range(len(bids)):
    NLabel = "favor{0}".format(bids[i])
    robot1 = Bot(task_queue1, db_config, NLabel)
    task_queue1.put(bids[i])
    robot1.run()
    print('------------------------书号:',bids[i],'爬取完毕-----------------------------')


cur.close()

#robot1.enqueue_boundary_books()
