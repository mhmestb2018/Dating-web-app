import json, mariadb, time
from retrying import retry

from ..utils.misc import retry_on_db_error

class Schema:
    def connect(self):
        self.conn = False
        while not self.conn:
            try:
                self.conn = mariadb.connect(**self.config)
            except mariadb.Error as e:
                print(f"Connection to database failed: {e}", flush=True)
                time.sleep(1)
        self.conn.auto_reconnect = True
        self.cur = self.conn.cursor()

    def __init__(self, config):
        self.config = config
        self.connect()
        # autocommit = True by default

        # Create users first as other tables will refer to it
        self.create_users_table()
        self.create_likes_table()
        self.create_block_table()

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
        bio text DEFAULT '' NOT NULL,
        views_count int DEFAULT 0 NOT NULL,
        likes_count int DEFAULT 0 NOT NULL,
        picture_1 varchar(1024),
        picture_2 varchar(1024),
        picture_3 varchar(1024),
        picture_4 varchar(1024),
        picture_5 varchar(1024),
        validated tinyint DEFAULT 0 NOT NULL,
        PRIMARY KEY (id)
        ) ENGINE=InnoDB;
        """

        self.cur.execute(query)

    def create_likes_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS likes (
        id int NOT NULL AUTO_INCREMENT,
        user_id int NOT NULL,
        liked int NOT NULL,
        
        PRIMARY KEY (id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (liked) REFERENCES users(id)
        ) ENGINE=InnoDB;
        """

        self.cur.execute(query)

    def create_block_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS blocks (
        id int NOT NULL AUTO_INCREMENT,
        user_id int NOT NULL,
        blocked int NOT NULL,
        
        PRIMARY KEY (id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (blocked) REFERENCES users(id)
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

    @retry(retry_on_exception=retry_on_db_error, wait_fixed=1000)
    def exec(self, query, args=()):
        self.cur.execute(query, args)
        return True

    # Not used yet
    def insert(self, table, fields, **kwargs):
        data = []
        for f in fields:
            data += ["'" + kwargs[f] + "'"]
        query = f"INSERT INTO {table} ({','.join(fields)}) VALUES ({','.join(data)})"
        return self.exec(query)
