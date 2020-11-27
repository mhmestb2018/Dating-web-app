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
                time.sleep(2)
        self.conn.auto_reconnect = True
        self.cur = self.conn.cursor()

    def __init__(self, config):
        self.config = config
        self.connect()
        # autocommit = True by default

        # Create users first as other tables will refer to it
        self.create_users_table()
        # self.populate_users_table()
        self.create_likes_table()
        self.create_blocks_table()
        self.create_resets_table()
        self.create_reports_table()
        self.create_visits_table()
        self.create_validations_table()
        self.create_tags_table()
        self.create_user_tags_table()
        self.create_messages_table()
        self.create_notifications_table()

    def create_users_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS users (
        id int NOT NULL AUTO_INCREMENT,
        first_name varchar(255) NOT NULL,
        last_name varchar(255) NOT NULL,
        email varchar(255) NOT NULL UNIQUE,
        password varchar(255) NOT NULL,
        sex varchar(63) DEFAULT 'other',
        orientation varchar(63) DEFAULT 'bisexual',
        bio text DEFAULT '' NOT NULL,
        views_count int DEFAULT 0 NOT NULL,
        likes_count int DEFAULT 0 NOT NULL,
        picture_1 varchar(1024),
        picture_2 varchar(1024),
        picture_3 varchar(1024),
        picture_4 varchar(1024),
        picture_5 varchar(1024),
        validated tinyint DEFAULT 0 NOT NULL,
        banned tinyint DEFAULT 0 NOT NULL,
        last_seen timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
        age int DEFAULT 18 NOT NULL,
        lat float DEFAULT 0 NOT NULL,
        lon float DEFAULT 0 NOT NULL,
        PRIMARY KEY (id)
        ) ENGINE=InnoDB;
        """

        self.cur.execute(query)

    def create_reports_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS reports (
        user_id int NOT NULL,
        reported int NOT NULL,
        date timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
        
        PRIMARY KEY (user_id, reported),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (reported) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

        self.cur.execute(query)

    def create_visits_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS visits (
        user_id int NOT NULL,
        visited int NOT NULL,
        date timestamp(6) DEFAULT CURRENT_TIMESTAMP NOT NULL,
        
        PRIMARY KEY (date),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (visited) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

        self.cur.execute(query)

    def create_likes_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS likes (
        user_id int NOT NULL,
        liked int NOT NULL,
        date timestamp(6) DEFAULT CURRENT_TIMESTAMP NOT NULL,
        
        PRIMARY KEY (date),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (liked) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

        self.cur.execute(query)

    def create_resets_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS resets (
        user_id int NOT NULL,
        reset_id varchar(128) NOT NULL,
        date timestamp(6) DEFAULT CURRENT_TIMESTAMP NOT NULL,
        
        PRIMARY KEY (date),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

        self.cur.execute(query)

    def create_validations_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS validations (
        user_id int NOT NULL,
        validation_id varchar(128) NOT NULL,
        date timestamp(6) DEFAULT NOW() NOT NULL,
        
        PRIMARY KEY (date),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

        self.cur.execute(query)

    def create_blocks_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS blocks (
        user_id int NOT NULL,
        blocked int NOT NULL,
        date timestamp(6) DEFAULT NOW() NOT NULL,
        
        PRIMARY KEY (date),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (blocked) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

        self.cur.execute(query)

    def create_tags_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS tags (
        id int NOT NULL AUTO_INCREMENT,
        name varchar(100) NOT NULL,
        
        PRIMARY KEY (id)
        ) ENGINE=InnoDB;
        """

        self.cur.execute(query)

    def create_user_tags_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS user_tags (
        user_id int NOT NULL,
        tag_id int NOT NULL,
        
        PRIMARY KEY (user_id, tag_id),
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES tags(id)
        ) ENGINE=InnoDB;
        """

        self.cur.execute(query)

    def create_messages_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS messages (
        from_id int NOT NULL,
        to_id int NOT NULL,
        content text NOT NULL,
        date timestamp(6) DEFAULT NOW() NOT NULL,
        unread int DEFAULT 1,
        
        PRIMARY KEY (date),
        FOREIGN KEY (from_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (to_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

        self.cur.execute(query)

    def create_notifications_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS notifications (
        from_id int NOT NULL,
        user_id int NOT NULL,
        type varchar(64) NOT NULL,
        date timestamp(6) DEFAULT NOW() NOT NULL,
        unread int DEFAULT 1,
        
        PRIMARY KEY (date),
        FOREIGN KEY (from_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
        """

        self.cur.execute(query)

# from_id, user_id, type, unread, date

    @retry(retry_on_exception=retry_on_db_error, wait_fixed=1000, stop_max_attempt_number=3)
    def exec(self, query, args=()):
        with mariadb.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute(query, args)
                return cur.lastrowid

    @retry(retry_on_exception=retry_on_db_error, wait_fixed=1000, stop_max_attempt_number=3)
    def fetch(self, query, args=()):
        with mariadb.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute(query, args)
                return cur.fetchall()
