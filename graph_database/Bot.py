from time import sleep
import traceback
from gdb_broker import neo4j_broker
from py2neo import NodeMatcher
from single_crawl import crawl_doubanbook_single_page, Task2


# 初始化要处理的任务内容,每一个节点为一本书,以及节点的延申节点


class Bot:
    def __init__(self, task_queue1, db_config, NLable):
        self.task_queue1 = task_queue1
        self.db_connection = neo4j_broker(db_config, task_queue1, NLable)
        self.NLable = NLable

    def run(self, max_crawl_pages=100):
        crawled_pages = 0
        while crawled_pages <= max_crawl_pages \
                and self.task_queue1.unfinished_tasks >= 1:
            task1 = self.task_queue1.get()
            if not self.db_connection.book_exists_by_bid(task1) \
                    or self.db_connection.is_boundary_book_by_bid(task1):
                for i in range(5):
                    try:
                        task2 = crawl_doubanbook_single_page(task1)
                        self.db_connection.add_new_book(task2)
                        if task2 is not None:
                            break
                    except Exception as inst:
                        print(type(inst))
                        print("error occurred when crawling book with id:{0}".format(task1))
                        print("crawling again!")
                        sleep(3)

            else:
                crawled_pages += 1
                print("successfully crawled book with id:{0}".format(task1))
                sleep(3)

            print("mission completed")

            if self.db_connection.node_num() >= 100:
                self.fill_books_info()
                self.task_queue1.queue.clear()
                return

    def fill_books_info(self):
        boundary_books_id = self.db_connection.get_boundary_books_id()
        trans = self.db_connection.graph.begin()
        info = {}
        for bid in boundary_books_id:
            for i in range(5):
                try:
                    info = crawl_doubanbook_single_page(bid).book_info
                    if info is not None:
                        break
                except Exception as e:
                    print("Error:", e)
                    print("error occurred when crawling book with id:{0}".format(bid))
                    # 请求失败再次请求
                    print("crawling again!")

            if info:
                node = NodeMatcher(self.db_connection.graph).match(self.NLable, bid=bid).first()
                node.update(**info)
                self.db_connection.graph.push(node)
                print('已经完善《', info["name"], '》相关信息')
            else:
                print('书号:', bid, '爬取失败')
        trans.commit()

    def enqueue_boundary_books(self):
        boundary_books_id = self.db_connection.get_boundary_books_id()
        for bid in boundary_books_id:
            self.task_queue1.put(bid)
