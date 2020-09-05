import json, mariadb, time

class Schema:
    def __init__(self, config):
        self.conn = False
        while not self.conn:
            try:
                self.conn = mariadb.connect(**config)
            except mariadb.Error as e:
                print(f"Connection to database failed: {e}", flush=True)
                time.sleep(1)
        # autocommit = True by default
        self.cur = self.conn.cursor()
        # Create users first as other tables will refer to it
        self.create_users_table()
        
        # self.populate_users_table()

    def create_users_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS users (
        id int NOT NULL AUTO_INCREMENT,
        first_name varchar(255) NOT NULL,
        last_name varchar(255) NOT NULL,
        email varchar(255) NOT NULL,
        password varchar(255) NOT NULL,
        sex varchar(63),
        orientation varchar(63),
        bio text,
        views_count int,
        likes_count int,
        main_picture varchar(1024),
        validated bit,
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

    