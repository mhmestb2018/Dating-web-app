import json, mariadb

class Schema:
    def __init__(self, config):
        self.conn = False
        while not self.conn:
            self.conn = mariadb.connect(**config)
        # autocommit = True by default
        self.cur = self.conn.cursor()
        # Create users first as other tables will refer to it
        self.create_users_table()
        self.populate_users_table()

    def create_users_table(self):

        self.cur.execute("DROP TABLE IF EXISTS users")

        query = """
        CREATE TABLE IF NOT EXISTS users (
        id int NOT NULL AUTO_INCREMENT,
        first_name varchar(255) NOT NULL,
        last_name varchar(255) NOT NULL,
        email varchar(255) NOT NULL,
        password varchar(255) NOT NULL,
        PRIMARY KEY (id)
        ) ENGINE=InnoDB;
        """

        self.cur.execute(query)

    def populate_users_table(self):
        query = """
        INSERT INTO users (first_name, last_name, email, password) VALUES
        ('Toto', 'gjhh', 'gdssgs', 'sgsssg'),
        ('Jack', 'gjgh', 'gdsss', 'ssssgd'),
        ('Titi', 'ghgh', 'gssgs', 'sgsssd');
        """
        self.cur.execute(query)

    def exec(self, query, args=()):
        # if mariadb.mysql_ping(self.conn):
        self.cur.execute(query, args)

        ### DEBUG ###
        # for val in self.cur.fetchall()[0]:
        #     print(val, flush=True)
        return True
        # return False

    # Not used yet
    def insert(self, table, fields, **kwargs):
        data = []
        for f in fields:
            data += ["'" + kwargs[f] + "'"]
        query = f"INSERT INTO {table} ({','.join(fields)}) VALUES ({','.join(data)})"
        return self.exec(query)

    