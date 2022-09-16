import pymysql

from typing import List
from settings import db_host, db_port,db_user, db_password, db_name, categories_table
from loguru import logger


class DataBaseHandler:
    def __init__(self):
        logger.debug('Сonnecting to a remote database')
        self.mysql_connection = pymysql.connect(host=db_host,
                                                port=db_port,
                                                user=db_user,
                                                password=db_password,
                                                database=db_name,
                                                charset='utf8mb4',
                                                autocommit=True)
        self.mysql_cursor = self.mysql_connection.cursor()
        self.mysql_connection.autocommit(True)
        
        # Проверка и создание отсутствующих таблицы
        logger.debug('Checking the om "viewed_links_youla" table')
        self.mysql_cursor.execute("""
        CREATE TABLE IF NOT EXISTS viewed_links_youla (
        url	VARCHAR(200) NOT NULL UNIQUE)""")

        # logger.debug('Checking the om "stopwords_youla" table')
        # self.mysql_cursor.execute("""
        # CREATE TABLE IF NOT EXISTS stopwords_youla (
        # word VARCHAR(200) NOT NULL)""")

        logger.debug(f'Checking the om {categories_table} table')
        self.mysql_cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {categories_table} (
        url	VARCHAR(400) NOT NULL UNIQUE)""")

        # logger.debug('Checking the om "blacklist_youla" table')
        # self.mysql_cursor.execute("""
        # CREATE TABLE IF NOT EXISTS blacklist_youla (
        # seller_id	VARCHAR(200) NOT NULL,
        # PRIMARY KEY(seller_id))""")

        logger.info('DataBaseHandler - ready!')

    def get_viewed_links(self) -> List:
        logger.debug('Getting viewed links')
        while True:
            try:
                self.mysql_cursor.execute("SELECT url FROM viewed_links_youla")
                resp = self.mysql_cursor.fetchall()
            except pymysql.err.OperationalError:
                self.mysql_connection.ping(True)

            else:
                break
        logger.debug('Viewed links received')
        return [d[0] for d in resp]

    def add_to_viewed_links(self, url: str):
        logger.debug(f'Adding to viewed links - {url}')
        while True:
            try:
                self.mysql_cursor.execute("INSERT INTO viewed_links_youla VALUES(%s)", (url,))
                self.mysql_connection.commit()
            except pymysql.err.OperationalError:
                self.mysql_connection.ping(True)

            except pymysql.err.IntegrityError:
                break
            else:
                break
        logger.debug('The url has been added to viewed links')

    def get_categories(self) -> List:
        self.mysql_connection.ping(True)

        logger.debug('Getting categories')
        self.mysql_cursor.execute(f"SELECT url FROM {categories_table}")
        resp = self.mysql_cursor.fetchall()
        logger.debug('Categories received')
        return [d[0] for d in resp]

    # def get_blacklist(self) -> List:
    #     self.mysql_connection.ping(True)
    #
    #     logger.debug('Getting blacklist')
    #     self.mysql_cursor.execute("SELECT seller_id FROM blacklist_youla")
    #     resp = self.mysql_cursor.fetchall()
    #
    #     return [d[0] for d in resp]

    # def get_stopwords(self) -> List:
    #     self.mysql_connection.ping(True)
    #     logger.debug('Getting stopwords')
    #     self.mysql_cursor.execute("SELECT word FROM stopwords")
    #     resp = self.mysql_cursor.fetchall()
    #
    #     return [d[0] for d in resp]


if __name__ == '__main__':
    db = DataBaseHandler()
    print(db.get_categories())