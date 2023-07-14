import time
import traceback
from graph_database.gdb_broker import neo4j_broker
from py2neo import NodeMatcher
from single_crawl import crawl_doubanbook_single_page,Task2
from time import sleep

# 初始化要处理的任务内容,每一个节点为一本书,以及节点的延申节点


class Bot:
    def __init__(self, task_queue1, db_config):
        self.task_queue1 = task_queue1
        self.db_connection = neo4j_broker(db_config, task_queue1)

    def run(self, max_crawl_pages=100):
        crawled_pages = 0
        while crawled_pages <= max_crawl_pages and self.task_queue1.unfinished_tasks >= 1:
            task1 = self.task_queue1.get()
            if not self.db_connection.book_exists_by_bid(task1) or self.db_connection.is_boundary_book_by_bid(task1):
                try:
                    task2 = crawl_doubanbook_single_page(task1)
                    self.db_connection.add_new_book(task2)

                except Exception as inst:
                    print(type(inst))
                    print("error occurred when crawling book with id:{0}".format(task1))
                    traceback.print_exc()
            else:
                crawled_pages += 1
                print("successfully crawled book with id:{0}".format(task1))
                time.sleep(3)
            print("mission completed")

            if self.task_queue1.qsize() >= 100:
                self.fill_books_info()
                return

    def fill_books_info(self):
        boundary_books_id = self.db_connection.get_boundary_books_id()
        trans = self.db_connection.graph.begin()
        for bid in boundary_books_id:
            info = crawl_doubanbook_single_page(bid).book_info
            node = NodeMatcher(self.db_connection.graph).match("Book", bid=bid).first()
            node.update(**info)
            self.db_connection.graph.push(node)
            print('已经完善《', info["name"], '》相关信息')
            sleep(3)
        trans.commit()

    def enqueue_boundary_books(self):
        boundary_books_id = self.db_connection.get_boundary_books_id()
        for bid in boundary_books_id:
            self.task_queue1.put(bid)