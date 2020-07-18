# import sqlalchemy
# import os


class Schema:
    pass
    # def __init__(self):
    #     config = {
    #         'host': 'db',
    #         'port': 3306,
    #         'user': os.environ['MYSQL_USER'],
    #         'password': os.environ['MYSQL_PASSWORD'],
    #         'database': 'matcha',
    #     }
    #     self.conn = mariadb.connect(config)
    #     self.cur = self.conn.cursor()
    #     # Create users first as other tables will refer to it
    #     self.create_users_table()
    #     self.populate_users_table()

    # def create_users_table(self):

    #     query = """
    #     CREATE TABLE IF NOT EXISTS users (
    #     id int NOT NULL AUTO_INCREMENT,
    #     name varchar(32) NOT NULL,
    #     picture_url varchar(2083) NOT NULL,
    #     PRIMARY KEY (id)
    #     );
    #     """

    #     self.cur.execute(query)
    # def populate_users_table(self):
    #     # create user table in similar fashion
    #     # come on give it a try it's okay if you make mistakes
    #     query = """
    #     INSERT INTO users (name, picture_url) VALUES
    #     ('Toto', 'gjhgh'),
    #     ('Jack', 'gjhgh'),
    #     ('Titi', 'gjhgh');
    #     """
    #     self.cur.execute(query)
