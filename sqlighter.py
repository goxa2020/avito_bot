import logging
import sqlite3


class Sqlighter:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, check_same_thread=False)
        self.cursor = self.connection.cursor()
        logging.info("Подключение к базе данных успешно".upper())

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute(f'INSERT INTO users (user_id) VALUES({user_id})')

    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `users`").fetchall()

    def user_is_admin(self, user_id):
        with self.connection:
            return bool(len(self.cursor.execute(f'SELECT * FROM admins WHERE admin_id = {user_id}').fetchmany(1)))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))
    
    def add_admin(self, user_id, appointed_by, admin_name):
        with self.connection:
            return self.cursor.execute(f'INSERT INTO admins (admin_id, appointed_by, admin_name) '
                                       f'VALUES(?,?,?)', (user_id, appointed_by, admin_name))

    def get_admins(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `admins`").fetchall()

    def del_admin(self, admin_id):
        with self.connection:
            return self.cursor.execute(f'DELETE FROM admins WHERE `admin_id` = {admin_id}')

    def get_admin_name(self, admin_id):
        with self.connection:
            return self.cursor.execute(f'SELECT admin_name FROM admins WHERE admin_id = {admin_id}').fetchmany(1)[0][0]

    def add_ad(self, user_name, product_name, amount, price, town, picture_id, user_id, description, posted = False):
        posted = posted or False
        with self.connection:
            return self.cursor.execute(
                f'INSERT INTO ads (user_name, product_name, amount, price, town, picture_id, user_id, description, posted) '
                f'VALUES(?,?,?,?,?,?,?,?,?)',
                (user_name, product_name, amount, price, town, picture_id, user_id, description, posted))

    def get_ads(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `ads`").fetchall()

    def del_ad(self, ad_id):
        with self.connection:
            return self.cursor.execute(f'DELETE FROM ads WHERE `ad_id` = {ad_id}')

    # def add_posted_ad(self, user_name, product_name, product_amount, product_price, town, picture_id, user_id, description, post_id):
    #     with self.connection:
    #         return self.cursor.execute(f'INSERT INTO posted_ads (user_name, product_name, product_amount, product_price, town, picture_id, user_id, description) '
    #                                    f'VALUES(?,?,?,?,?,?,?,?)', (user_name, product_name, product_amount, product_price, town, picture_id, user_id, description))
    #
    # def get_posted_ads(self):
    #     with self.connection:
    #         return self.cursor.execute("SELECT * FROM `ad_for_add`").fetchall()
    #
    # def del_posted_ad(self, ad_id):
    #     with self.connection:
    #         return self.cursor.execute(f'DELETE FROM ad_for_add WHERE `ad_id` = {ad_id}')

    def close(self):
        self.connection.close()
# i love u