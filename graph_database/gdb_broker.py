from py2neo import Graph, Node, Relationship


class neo4j_broker:
    def __init__(self, db_config, task_queue1, NLable):
        host = db_config["host"]
        username = db_config["user"]
        password = db_config["password"]
        self.graph = Graph(host, auth=(username, password))
        self.task_queue1 = task_queue1
        self.NLable = NLable

    def connection_test(self):
        trans = self.graph.begin()  # 用Transaction

        node_1 = Node("Person", name="Alpha")
        node_2 = Node("Person", name="Beta")
        rel = Relationship(node_1, "KNOWS", node_2)
        self.graph.create(rel)
        trans.commit()

    def node_num(self):
        num = self.graph.run("MATCH (n:{0}) RETURN COUNT(n) as num".format(self.NLable)).data()
        return int(num[0]['num'])

    def clear_db(self):
        self.graph.run("MATCH (n:{0}) DETACH DELETE n".format(self.NLable))

    def book_exists_by_bid(self, bid):
        cur = self.graph.run('MATCH (n:{0} {{bid: "{1}"}}) return n;'.format(self.NLable, bid))
        if not cur.data():
            return False
        else:
            return True

    def is_boundary_book_by_bid(self, bid):
        cur = self.graph.run('MATCH (b:{0}) WHERE b.bid="{1}" AND NOT (b)-[:读者可能喜欢]->(:{2}) RETURN b;'
                             .format(self.NLable, bid, self.NLable))
        if not cur.data():
            return False
        else:
            return True

    def merge_book_with_property(self, bid, prop_dict: dict):
        query = 'MERGE (n:{0} {{bid: "{1}"}}) SET'.format(self.NLable, bid)

        prop_idx = 1
        badchar = {'\'': '‘', '\"': '“'}
        for prop in prop_dict:
            if type(prop_dict[prop]) == list:
                temp = ""
                for i in range(0, len(prop_dict[prop])):
                    if type(prop_dict[prop][i]) == str:
                        for c in badchar:
                            prop_dict[prop][i] = str.replace(prop_dict[prop][i], c, badchar[c])
                    temp += prop_dict[prop][i]
                    if i < len(prop_dict[prop]) - 1:
                        temp += ","

                query += " n.{0}='{1}'".format(prop, temp)
                pass
            else:
                if type(prop_dict[prop]) == str:
                    for c in badchar:
                        prop_dict[prop] = str.replace(prop_dict[prop], c, badchar[c])
                query += " n.{0}='{1}'".format(prop, prop_dict[prop])

            if prop_idx < len(prop_dict):
                query += ','
                prop_idx += 1
        self.graph.run(query)

    def create_books_rel(self, bid1, bid2):
        query = "MATCH (B1:{0} {{bid:'{1}'}}), (B2:{2} {{bid:'{3}'}}) MERGE (B1)-[:读者可能喜欢]->(B2)" \
            .format(self.NLable, bid1, self.NLable, bid2)
        self.graph.run(query)

    def add_new_book(self, task2):
        b_info = task2.book_info
        books_rec_ids = task2.books_rec_ids
        books_rec_names = task2.books_rec_names

        if not self.book_exists_by_bid(b_info["bid"]):
            trans = self.graph.begin()
            node_1 = Node(self.NLable, **b_info)
            for i in range(0, len(books_rec_ids)):
                if not self.book_exists_by_bid(books_rec_ids[i]):
                    node_temp = Node(self.NLable, bid=books_rec_ids[i], name=books_rec_names[i])
                    rel = Relationship(node_1, "读者可能喜欢", node_temp)
                    self.graph.create(rel)
                    self.task_queue1.put(books_rec_ids[i])
                else:
                    self.create_books_rel(b_info["bid"], books_rec_ids[i])
                    pass
            trans.commit()
        else:
            self.merge_book_with_property(b_info["bid"], b_info)
            for i in range(0, len(books_rec_ids)):
                if not self.book_exists_by_bid(books_rec_ids[i]):
                    node_temp = Node(self.NLable, bid=books_rec_ids[i], name=books_rec_names[i])
                    self.graph.create(node_temp)
                    self.graph.push(node_temp)
                    self.create_books_rel(b_info["bid"], books_rec_ids[i])
                    self.task_queue1.put(books_rec_ids[i])
                else:
                    self.create_books_rel(b_info["bid"], books_rec_ids[i])

    def get_boundary_books_id(self):
        boundary_books_id = []
        cur = self.graph.run("MATCH (b:{0}) WHERE NOT (b)-[:读者可能喜欢]->(:{1}) RETURN b".format(self.NLable, self.NLable))
        if cur is not None:
            for node in cur:
                bid = node.data()['b']['bid']
                boundary_books_id.append(bid)
        return boundary_books_id

